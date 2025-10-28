import os
import shutil
import logging
import tempfile
import pytest
import allure
import time
import config.env_config as env_config
from pathlib import Path
from filelock import FileLock
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pages.base.page_manager import PageManager
from utils.logging_helper import configure_root_logger, set_current_test
from utils.video_recorder import start_video_recording

# Configure root logger once for the test session
root_logger = configure_root_logger(log_file="test_logs.log", level=logging.INFO)


"""

Pytest Fixtures - Scope = function

"""


@pytest.fixture(scope="function")
def driver(request):
    """
    Initialize driver at the start of each test.
    """
    browser = request.config.getoption("--browser", default=env_config.BROWSER.lower())
    root_logger.debug(f"Initializing driver for browser: {browser} (Config: {env_config.BROWSER.lower()}).")

    # try to get the user_data_dir that was set by unique_user_data_dir; if missing create a temp one
    user_data_dir = getattr(request.config, "user_data_dir", None)
    if not user_data_dir:
        # per-test fallback
        worker = os.environ.get("PYTEST_XDIST_WORKER", f"local_{os.getpid()}")
        user_data_dir = Path(tempfile.gettempdir()) / f"user_data_{worker}_{int(time.time())}"
        user_data_dir.mkdir(parents=True, exist_ok=True)
    root_logger.debug(f"Using user_data_dir: {user_data_dir}")

    # compute a stable-ish integer suffix for a debugging port to avoid CDP collisions
    worker_token = os.environ.get("PYTEST_XDIST_WORKER", str(os.getpid()))
    port_suffix = int("".join(ch for ch in worker_token if ch.isdigit()) or "0") % 1000
    debug_port = 9222 + port_suffix  # keep port in reasonable range
    root_logger.debug(f"Using debug_port: {debug_port}")

    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Use the per-worker user-data-dir
        chrome_options.add_argument(
            f"--remote-debugging-port={debug_port}"
        )  # avoid DevTools port collisions between workers
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-gpu")  # If there are GPU related issues
        chrome_options.add_argument("--no-sandbox")  # If there are sandbox related issues
        chrome_options.add_argument("--disable-dev-shm-usage")  # If there are memory related issues
        if env_config.MAXIMIZED:
            chrome_options.add_argument("--start-maximized")
        if env_config.HEADLESS:
            chrome_options.add_argument("--headless=new")

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Ensure even viewport size to avoid odd-dimension frames (helps ffmpeg/libx264)
        try:
            driver.set_window_size(1920, 1080)  # use even width/height appropriate for CI
        except Exception:
            # ignore if not supported in current environment
            pass

    elif browser == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("dom.webdriver.enabled", False)
        firefox_options.set_preference("dom.push.enabled", False)
        firefox_options.set_preference("javascript.enabled", True)
        if env_config.HEADLESS:
            firefox_options.add_argument("--headless=new")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        if env_config.MAXIMIZED:
            driver.maximize_window()

    else:
        raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'firefox'.")

    try:
        yield driver
    finally:
        root_logger.info(f"Quitting driver for browser: {browser}.")
        driver.quit()


@pytest.fixture(scope="function")
def page_manager(driver, logger):
    """
    Initialize PageManager object with driver and logger.
    Navigates to BASE_URL at the start of each test.
    """
    pm = PageManager(driver, logger)
    pm.navigate_to_base_url(env_config.BASE_URL)
    return pm


@pytest.fixture(scope="function", autouse=True)
def test_context(request):
    """
    Sets current test name at the start of each test for logging purposes.
    """
    test_name = request.node.name
    set_current_test(test_name)
    root_logger.info(f"Starting test: {test_name}.")
    yield


@pytest.fixture(scope="function", autouse=True)
def video_recorder(request, driver, logger):
    if not getattr(env_config, "VIDEO_RECORDING", False):
        yield
        return

    if not isinstance(driver, webdriver.Chrome):
        yield
        return

    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "local")
    test_name = request.node.name.replace(":", "_").replace("/", "_")

    stop_func, video_path = start_video_recording(driver, test_name, worker_id)
    logger.info(f"Started recording: {video_path}")

    yield

    logger.info("Stopping video recording...")
    stop_func()


@pytest.fixture(scope="function")
def actions(driver):
    return ActionChains(driver)


"""

Pytest Fixtures - Scope = session

"""


@pytest.fixture(scope="session")
def logger():
    """
    Makes the root logger accessible to other files.
    """
    return root_logger


@pytest.fixture(scope="session", autouse=True)
def unique_user_data_dir(request):
    # Robustly determine worker id (xdist sets PYTEST_XDIST_WORKER env var and request.config.workerinput in workers)
    try:
        worker_id = request.config.workerinput.get("workerid")
    except Exception:
        worker_id = os.environ.get("PYTEST_XDIST_WORKER", "local")

    # Fallback to a safe string and ensure unique per worker
    if not worker_id:
        worker_id = f"local_{os.getpid()}"

    user_data_dir = Path(tempfile.gettempdir()) / f"user_data_{worker_id}"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    request.config.user_data_dir = user_data_dir
    yield


@pytest.fixture(scope="session", autouse=True)
def clean_allure_report():
    """
    Cleans Allure Report folder(s) at the start of each session.
    """
    allure_report_dir = Path("reports") / "allure-report"
    lock_file = allure_report_dir / "allure-report.lock"
    allure_report_dir.parent.mkdir(parents=True, exist_ok=True)
    # Use a file lock to prevent race conditions in parallel execution
    with FileLock(lock_file):
        if allure_report_dir.exists():
            shutil.rmtree(allure_report_dir, ignore_errors=True)  # Safely remove directory
        allure_report_dir.mkdir(parents=True, exist_ok=True)  # Recreate empty directory


@pytest.fixture(scope="session", autouse=True)
def clean_screenshots_at_start():
    """
    Cleans tests screenshots folder at the start of each session.
    """
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "local")
    screenshots_dir = Path("tests_screenshots") / worker_id
    lock_file = screenshots_dir / f"{worker_id}.lock"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    with FileLock(lock_file):
        if screenshots_dir.exists():
            shutil.rmtree(screenshots_dir, ignore_errors=True)
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        root_logger.info(f"Screenshots directory cleaned and recreated at: {screenshots_dir}.")


@pytest.fixture(scope="session", autouse=True)
def clean_videos_at_start():
    """
    Cleans tests recordings folder at the start of each session.
    """
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "local")
    videos_dir = Path("tests_recordings") / worker_id
    lock_file = videos_dir / f"{worker_id}.lock"
    videos_dir.mkdir(parents=True, exist_ok=True)
    with FileLock(lock_file):
        if videos_dir.exists():
            shutil.rmtree(videos_dir, ignore_errors=True)
        videos_dir.mkdir(parents=True, exist_ok=True)
        root_logger.info(f"Videos directory cleaned and recreated at: {videos_dir}.")


"""

Pytest Hooks

"""


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.user_data_dir = unique_user_data_dir


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    if not hasattr(session.config, "user_data_dir"):
        pytest.exit("User data directory not set.")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to handle:
    - Test duration logging.
    - Screenshot taking on test faliure (Locally and to Allure Report).
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        test_name = item.name
        duration = report.duration if hasattr(report, "duration") else 0
        root_logger.info(f"Finished test: {test_name} (Duration: {duration:.2f}s).")

        driver = item.funcargs.get("driver")
        if report.failed and driver:
            root_logger.info(f"Test {test_name} failed, capturing screenshot.")
            # Use worker ID to create unique screenshot directory for each parallel worker
            worker_id = os.environ.get("PYTEST_XDIST_WORKER", "local")
            screenshot_dir = Path("tests_screenshots") / worker_id
            screenshot_filename = (
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_" f"{test_name.replace(':', '_').replace('/', '_')}.png"
            )
            screenshot_path = Path(screenshot_dir) / screenshot_filename
            lock_file = Path(screenshot_dir) / f"{worker_id}.lock"

            try:
                # Ensure directory exists before creating/using the lock
                os.makedirs(screenshot_dir, exist_ok=True)
                # Acquire a lock inside the existing directory while writing the screenshot
                with FileLock(lock_file):
                    root_logger.debug(f"Attempting to save screenshot to: {screenshot_path}.")
                    driver.save_screenshot(screenshot_path)
                root_logger.info(f"Screenshot saved successfully to: {screenshot_path}.")
                if allure:
                    try:
                        allure.attach.file(
                            screenshot_path,
                            name=f"Failed_Screenshot_{test_name}",
                            attachment_type=allure.attachment_type.PNG,
                        )
                        root_logger.info(f"Screenshot attached to Allure report for {test_name}.")
                    except Exception as e:
                        root_logger.warning(f"Failed to attach screenshot to Allure report: {str(e)}.")
            except Exception as e:
                root_logger.error(f"Failed to save screenshot to {screenshot_path}: {str(e)}.")

    if report.when == "teardown":
        set_current_test(None)

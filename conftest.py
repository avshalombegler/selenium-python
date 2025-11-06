from __future__ import annotations
from typing import TYPE_CHECKING, Generator
import os
import shutil
import logging
import tempfile
import pytest
import allure
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

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from _pytest.fixtures import FixtureRequest
    from logging import Logger

DEBUG_PORT_BASE = 9222
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

# Configure root logger once for the test session
root_logger = configure_root_logger(log_file="test_logs.log", level=logging.INFO)


"""

Helper Functions

"""


def build_chrome_options(user_data_dir: Path, debug_port: int) -> ChromeOptions:
    options = ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")  # Use the per-worker user-data-dir
    options.add_argument(f"--remote-debugging-port={debug_port}")  # avoid DevTools port collisions between workers
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")  # If there are GPU related issues
    options.add_argument("--no-sandbox")  # If there are sandbox related issues
    options.add_argument("--disable-dev-shm-usage")  # If there are memory related issues
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    if env_config.MAXIMIZED:
        options.add_argument("--start-maximized")
    if env_config.HEADLESS:
        options.add_argument("--headless=new")
    return options


def build_firefox_options(user_data_dir: Path, debug_port: int) -> FirefoxOptions:
    options = FirefoxOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--remote-debugging-port={debug_port}")
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.push.enabled", False)
    options.set_preference("javascript.enabled", True)
    if env_config.HEADLESS:
        options.add_argument("--headless=new")
    return options


def get_worker_id() -> str:
    return os.environ.get("PYTEST_XDIST_WORKER", "local") or f"local_{os.getpid()}"


def clean_directory(dir_path: Path, lock_suffix: str = "lock") -> None:
    """Helper to clean and recreate a directory with file locking."""
    lock_file = dir_path / f"{lock_suffix}.lock"
    dir_path.mkdir(parents=True, exist_ok=True)
    with FileLock(lock_file):
        if dir_path.exists():
            shutil.rmtree(dir_path, ignore_errors=True)
        dir_path.mkdir(parents=True, exist_ok=True)
        root_logger.info(f"Directory cleaned and recreated at: {dir_path}.")


def save_screenshot_on_failure(driver: WebDriver, test_name: str) -> None:
    root_logger.info(f"Test {test_name} failed, capturing screenshot.")
    # Use worker ID to create unique screenshot directory for each parallel worker
    worker_id = get_worker_id()
    screenshot_dir = Path("tests_screenshots") / worker_id
    screenshot_filename = (
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_" f"{test_name.replace(':', '_').replace('/', '_')}.png"
    )
    screenshot_path = Path(screenshot_dir) / screenshot_filename
    lock_file = Path(screenshot_dir) / f"{worker_id}.lock"

    try:
        # Ensure directory exists before creating/using the lock
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        # Acquire a lock inside the existing directory while writing the screenshot
        with FileLock(lock_file):
            root_logger.debug(f"Attempting to save screenshot to: {screenshot_path}.")
            driver.save_screenshot(screenshot_path)
        root_logger.info(f"Screenshot saved successfully to: {screenshot_path}.")
        if allure is not None:
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


"""

Pytest Fixtures

"""


@pytest.fixture(scope="function")
def page_manager(driver: WebDriver, logger: Logger) -> PageManager:
    """
    Initialize PageManager object with driver and logger.
    """
    return PageManager(driver, logger)


@pytest.fixture(scope="function", autouse=True)
def ui_test(page_manager: PageManager, request: FixtureRequest) -> Generator[None, None, None]:
    """
    Navigate to base URL only for UI tests.
    Use: add @pytest.mark.ui to tests.
    """
    if request.node.get_closest_marker("ui"):
        with allure.step(f"Navigate to base URL: {env_config.BASE_URL}"):
            page_manager.navigate_to_base_url(env_config.BASE_URL)
    yield


@pytest.fixture(scope="function", autouse=True)
def test_context(request: FixtureRequest) -> Generator[None, None, None]:
    """
    Sets current test name at the start of each test for logging purposes.
    """
    test_name = request.node.name
    set_current_test(test_name)
    root_logger.info(f"Starting test: {test_name}.")
    yield


@pytest.fixture(scope="function", autouse=True)
def video_recorder(request: FixtureRequest, driver: WebDriver) -> Generator[None, None, None]:
    """
    Automatically records video of the test session using Chrome DevTools Protocol.
    Recording is enabled only if VIDEO_RECORDING is True in config and driver is Chrome.
    Skips recording for non-Chrome drivers or when disabled.
    """
    if not getattr(env_config, "VIDEO_RECORDING", False):
        yield
        return

    if not isinstance(driver, webdriver.Chrome):
        yield
        return

    worker_id = get_worker_id()
    test_name = request.node.name.replace(":", "_").replace("/", "_")

    stop_func, video_path = start_video_recording(driver, test_name, worker_id)
    root_logger.info(f"Started recording: {video_path}")

    yield

    root_logger.info("Stopping video recording...")
    stop_func()


@pytest.fixture(scope="function")
def actions(driver: WebDriver) -> ActionChains:
    """
    Provides a fresh ActionChains instance for the current WebDriver.
    Used for performing complex user interactions like drag-and-drop, right-click, etc.
    """
    return ActionChains(driver)


@pytest.fixture(scope="session")
def driver(request: FixtureRequest) -> Generator[WebDriver, None, None]:
    """
    Initialize driver object at the start of each test.
    """
    browser = request.config.getoption("--browser", default=env_config.BROWSER.lower())
    root_logger.debug(f"Initializing driver for browser: {browser} (Config: {env_config.BROWSER.lower()}).")

    # Get user_data_dir that was set by unique_user_data_dir
    user_data_dir = getattr(request.config, "user_data_dir", None)
    if user_data_dir is None:
        raise RuntimeError("user_data_dir not set by unique_user_data_dir fixture.")
    user_data_dir = Path(user_data_dir)
    root_logger.debug(f"Using user_data_dir: {user_data_dir}")

    # Compute a stable-ish integer suffix for a debugging port to avoid CDP collisions
    worker_token = os.environ.get("PYTEST_XDIST_WORKER", str(os.getpid()))
    port_suffix = int("".join(ch for ch in worker_token if ch.isdigit()) or "0") % 1000
    debug_port = DEBUG_PORT_BASE + port_suffix  # keep port in reasonable range
    root_logger.debug(f"Using debug_port: {debug_port}")

    try:
        driver: WebDriver
        if browser == "chrome":
            chrome_service = ChromeService(ChromeDriverManager().install())
            chrome_options = build_chrome_options(user_data_dir, debug_port)
            driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            # Ensure even viewport size
            try:
                driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
            except Exception:
                pass  # Ignore if not supported

        elif browser == "firefox":
            firefox_service = FirefoxService(GeckoDriverManager().install())  # Use separate variable
            firefox_options = build_firefox_options(user_data_dir, debug_port)
            driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
            if env_config.MAXIMIZED:
                driver.maximize_window()

        else:
            raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'firefox'.")

    except Exception as e:
        root_logger.error(f"Failed to initialize {browser} driver: {str(e)}")
        raise

    try:
        yield driver
    finally:
        root_logger.info(f"Quitting driver for browser: {browser}.")
        driver.quit()


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    """
    Makes the root logger accessible to other files.
    """
    return root_logger


@pytest.fixture(scope="session", autouse=True)
def unique_user_data_dir(request: FixtureRequest) -> Generator[None, None, None]:
    """
    Creates and yields a unique Chrome user data directory per test worker/session.
    Ensures isolation between parallel test runs (xdist) by using worker ID or PID.
    Directory is created in system temp and stored in config for driver setup.
    """
    try:
        worker_id = request.config.workerinput.get("workerid")  # type: ignore[attr-defined]
    except Exception:
        worker_id = get_worker_id()

    user_data_dir = Path(tempfile.gettempdir()) / f"user_data_{worker_id}"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    request.config.user_data_dir = user_data_dir  # type: ignore[attr-defined]
    yield


@pytest.fixture(scope="session", autouse=True)
def clean_allure_report() -> Generator[None, None, None]:
    allure_report_dir = Path("reports") / "allure-report"
    clean_directory(allure_report_dir, "allure-report")
    yield


@pytest.fixture(scope="session", autouse=True)
def clean_screenshots_at_start() -> None:
    worker_id = get_worker_id()
    screenshots_dir = Path("tests_screenshots") / worker_id
    clean_directory(screenshots_dir, worker_id)


@pytest.fixture(scope="session", autouse=True)
def clean_videos_at_start() -> None:
    worker_id = get_worker_id()
    videos_dir = Path("tests_recordings") / worker_id
    clean_directory(videos_dir, worker_id)


"""

Pytest Hooks

"""


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: "pytest.Config") -> None:
    """
    Sets the unique user data directory in pytest config during test setup.
    Ensures the directory created by the unique_user_data_dir fixture is available
    globally via config.user_data_dir for driver initialization and cleanup.
    """
    config.user_data_dir = unique_user_data_dir  # type: ignore[attr-defined]


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: "pytest.Session") -> None:
    """
    Validates that user_data_dir is set in pytest config at session start.
    Exits the test run with an error if the directory is missing, preventing
    driver initialization without isolation.
    """
    if not hasattr(session.config, "user_data_dir"):
        pytest.exit("User data directory not set.")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: "pytest.Item") -> Generator[None, None, None]:
    """
    Pytest hook to handle:
        - Test duration logging.
        - Screenshot taking on test faliure (Locally and to Allure Report).
    """
    outcome = yield
    report = outcome.get_result()  # type: ignore[attr-defined]

    if report.when == "call":
        test_name = item.name
        duration = report.duration if hasattr(report, "duration") else 0
        root_logger.info(f"Finished test: {test_name} (Duration: {duration:.2f}s).")

        driver = item.funcargs.get("driver")  # type: ignore[attr-defined]
        if report.failed and driver:
            save_screenshot_on_failure(driver, test_name)

    if report.when == "teardown":
        set_current_test(None)

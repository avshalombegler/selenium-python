import os
import shutil
import logging
import pytest
import allure
import time
import config.env_config as env_config
from pyscreenrec import ScreenRecorder
from mss import mss
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pages.page_manager import PageManager
from utils.logging_helper import configure_root_logger, set_current_test

# Configure root logger once for the test session
root_logger = configure_root_logger(log_file="test_logs.log", level=logging.INFO)


@pytest.fixture(scope="session")
def logger():
    """
    Makes the root logger accessible to other files.
    """
    return root_logger


@pytest.fixture(scope="function", autouse=True)
def test_context(request):
    """
    Sets current test name at the start of each test for logging purposes.
    """
    test_name = request.node.name
    set_current_test(test_name)
    root_logger.info(f"Starting test: {test_name}.")
    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to handle:
        Test duration logging.
        Screenshot taking on test faliure (Locally and to Allure Report).
    """
    outcome = yield
    report = outcome.get_result()

    # Only handle "call" phase for finish logging and screenshots (this gives accurate duration)
    if report.when == "call":
        test_name = item.name
        duration = report.duration if hasattr(report, "duration") else 0
        root_logger.info(f"Finished test: {test_name} (Duration: {duration:.2f}s).")

        driver = item.funcargs.get("driver")
        if report.failed and driver:
            root_logger.info(f"Test {test_name} failed, capturing screenshot.")
            screenshot_filename = (
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_" f"{test_name.replace(':', '_').replace('/', '_')}.png"
            )
            screenshot_path = os.path.join("tests_screenshots", test_name, screenshot_filename)
            try:
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
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

    # Clear test context only after teardown phase so teardown/fixture finalizers still log with test prefix
    if report.when == "teardown":
        set_current_test(None)


@pytest.fixture(scope="function")
def driver(request):
    """
    Initialize driver at the start of each test.
    """
    browser = request.config.getoption("--browser", default=env_config.BROWSER.lower())
    root_logger.info(f"Initializing driver for browser: {browser} (Config: {env_config.BROWSER.lower()}).")

    if browser == "chrome":
        chrome_options = ChromeOptions()
        # Use platform-appropriate user-data-dir
        if os.name == 'nt':  # Windows
            chrome_options.add_argument("--user-data-dir=C:\\Temp\\ChromeProfile")
        else:  # Linux (CI)
            chrome_options.add_argument("--user-data-dir=/tmp/chrome-profile")
        if env_config.MAXIMIZED:
            chrome_options.add_argument("--start-maximized")
        # More suitable for CI/CD run.
        if env_config.HEADLESS:
            chrome_options.add_argument("--headless=new")
        # chrome_options.add_argument("--disable-popup-blocking")
        # chrome_options.add_argument("--disable-notifications")
        # chrome_options.add_argument("--disable-gpu")  # If there are GPU related issues
        # chrome_options.add_argument("--no-sandbox")  # If there are sandbox related issues
        # chrome_options.add_argument("--disable-dev-shm-usage")  # If there are memory related issues
        # chrome_options.add_argument("--disable-background-networking")  # If there are network related issues
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)

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
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)

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


@pytest.fixture(scope="session", autouse=True)
def clean_allure_results():
    """
    Cleans Allure Report folder(s) at the start of each session.
    """
    # Clean both allure-results and allure-report folders.
    allure_results_dir = "reports/allure-results"
    allure_report_dir = "reports/allure-report"
    for dir_path in [allure_results_dir, allure_report_dir]:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path, exist_ok=True)

    # Clean only allure-report folder.
    # allure_results_dir = "reports/allure-report"
    # if os.path.exists(allure_report_dir):
    #     shutil.rmtree(allure_report_dir)
    #     os.makedirs(allure_report_dir, exist_ok=True)


@pytest.fixture(scope="session", autouse=True)
def clean_screenshots_at_start():
    """
    Cleans tests screenshots folder at the start of each session.
    """
    tests_screenshots_dir = "tests_screenshots"
    if os.path.exists(tests_screenshots_dir):
        shutil.rmtree(tests_screenshots_dir)
    os.makedirs(tests_screenshots_dir, exist_ok=True)
    root_logger.info(f"Screenshots directory cleaned and recreated at: {tests_screenshots_dir}.")


@pytest.fixture(scope="session", autouse=True)
def clean_videos_at_start():
    """
    Cleans tests recordings folder at the start of each session.
    """
    videos_dir = "tests_recordings"
    if os.path.exists(videos_dir):
        shutil.rmtree(videos_dir)
    os.makedirs(videos_dir, exist_ok=True)
    root_logger.info(f"Videos directory cleaned and recreated at: {videos_dir}.")


@pytest.fixture(scope="function", autouse=True)
def video_recorder(request, logger):
    """
    Handle test video recording.
    Set On/Off from VIDEO_RECORDING in confing.py.
    """
    if not env_config.VIDEO_RECORDING:
        logger.info("Video recording is disabled in config.py.")
        yield
        return

    test_name = request.node.name.replace(":", "_").replace("/", "_")
    videos_dir = "tests_recordings"
    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    video_path = os.path.join(videos_dir, f"{test_name}_{timestamp}.mp4")

    logger.info(f"Starting video recording for test {test_name} to: {video_path}.")

    sct = mss()
    monitor = sct.monitors[1]
    region = {
        "mon": 0,
        "left": monitor["left"],
        "top": monitor["top"],
        "width": monitor["width"],
        "height": monitor["height"],
    }

    recorder = ScreenRecorder()

    recorder.start_recording(video_path, 10, region)

    yield

    recorder.stop_recording()
    logger.info(f"Video saved to: {video_path}.")

    allure.attach.file(video_path, name=f"Video for {test_name}", attachment_type=allure.attachment_type.MP4)


@pytest.fixture(scope="function")
def actions(driver):
    return ActionChains(driver)

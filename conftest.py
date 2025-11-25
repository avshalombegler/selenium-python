from __future__ import annotations

import logging
import os
import shutil
import tempfile
from collections.abc import Generator
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import allure
import pytest
from _pytest.main import Session
from _pytest.nodes import Item
from filelock import FileLock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.firefox import GeckoDriverManager

import config.conftest_config as conftest_config
import config.env_config as env_config
from pages.base.page_manager import PageManager
from utils.logging_helper import configure_root_logger, set_current_test
from utils.video_recorder import start_video_recording

CACHE_VALID_RANGE = 30  # Days to keep cache valid

if TYPE_CHECKING:
    from logging import Logger

    from _pytest.fixtures import FixtureRequest
    from selenium.webdriver.remote.webdriver import WebDriver

DEBUG_PORT_BASE = 9222
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

# Configure root logger once for the test session
root_logger = configure_root_logger(log_file="test_logs.log", level=logging.INFO)

# ============================================================================
# HELPER METHODS
# ============================================================================


def get_chrome_driver_path() -> str:
    """Get ChromeDriver path with extended cache and error handling."""
    try:
        cache_manager = DriverCacheManager(valid_range=CACHE_VALID_RANGE)
        return ChromeDriverManager(cache_manager=cache_manager).install()
    except Exception as e:
        root_logger.warning(f"Failed to download ChromeDriver: {e}")
        # Fallback: try to use system chromedriver
        system_path = shutil.which("chromedriver")
        if system_path:
            root_logger.info(f"Using system ChromeDriver: {system_path}")
            return system_path
        raise RuntimeError("ChromeDriver not found. Install manually or check GitHub API limits.")


def get_firefox_driver_path() -> str:
    """Get GeckoDriver path with extended cache and error handling."""
    try:
        cache_manager = DriverCacheManager(valid_range=CACHE_VALID_RANGE)
        return GeckoDriverManager(cache_manager=cache_manager).install()
    except Exception as e:
        root_logger.warning(f"Failed to download GeckoDriver: {e}")
        # Fallback: try to use system geckodriver
        system_path = shutil.which("geckodriver")
        if system_path:
            root_logger.info(f"Using system GeckoDriver: {system_path}")
            return system_path
        raise RuntimeError("GeckoDriver not found. Install manually or check GitHub API limits.")


def build_chrome_options(user_data_dir: Path, downloads_directory: Path, debug_port: int) -> ChromeOptions:
    options = ChromeOptions()

    # Core arguments (order matters!)
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--profile-directory=Default")
    options.add_argument(f"--remote-debugging-port={debug_port}")

    # Disable profile reset BEFORE other args
    options.add_argument("--disable-features=TriggeredProfileReset,ProfileResetPrompt")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    # Media stream arguments
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")

    # Stability arguments
    for arg in [
        "--disable-popup-blocking",
        "--disable-notifications",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
    ]:
        options.add_argument(arg)

    # Consolidated preferences
    options.add_experimental_option(
        "prefs",
        {
            # Download preferences
            "download.default_directory": str(downloads_directory.resolve()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            # Notification and credential preferences
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.geolocation": 1,
            # Disable password manager
            "credentials_enable_service": False,  # Disable password manager
            "profile.password_manager_enabled": False,  # Disable password manager UI
            "profile.password_manager_leak_detection": False,  # Disable leak detection
            "autofill.profile_enabled": False,  # Disable autofill
            # Disable profile reset prompt
            "profile.exit_type": "Normal",
            "profile.exited_cleanly": True,
            # Disable various automation detection features
            "profile.default_content_settings.popups": 0,
            # Disable profile reset prompt
            "profile.reset_prompt_memento": {
                "prompt_shown_count": 0,
                "last_reset_time": 0,
                "last_reset_version": "",
            },
            "profile.reset_prompt_enabled": False,
        },
    )

    # Exclude automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)

    # Window and headless modes
    if env_config.MAXIMIZED:
        options.add_argument("--start-maximized")
    if env_config.HEADLESS:
        options.add_argument("--headless=new")

    return options


def build_firefox_options(user_data_dir: Path, downloads_directory: Path) -> FirefoxOptions:
    options = FirefoxOptions()

    # Clean existing profile directory
    if user_data_dir.exists():
        shutil.rmtree(user_data_dir, ignore_errors=True)
    user_data_dir.mkdir(parents=True, exist_ok=True)

    profile = webdriver.FirefoxProfile(str(user_data_dir))
    options.profile = profile

    # Geolocation preferences
    profile.set_preference("geo.prompt.testing", True)
    profile.set_preference("geo.prompt.testing.allow", True)
    profile.set_preference("geo.enabled", True)
    profile.set_preference("geo.provider.use_corelocation", False)
    profile.set_preference("geo.provider.testing", False)  # Set to False for manual override

    # Cache preferences
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)

    # Download preferences
    profile.set_preference("browser.download.dir", str(downloads_directory.resolve()))
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.manager.closeWhenDone", True)
    profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,text/plain,application/pdf"
    )
    profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
    profile.set_preference("browser.download.manager.focusWhenStarting", False)
    profile.set_preference("browser.download.manager.useWindow", False)
    profile.set_preference("browser.download.manager.showAlertOnComplete", False)

    # Password manager preferences
    profile.set_preference("signon.rememberSignons", False)
    profile.set_preference("signon.autofillForms", False)
    profile.set_preference("signon.management.page.breach-alerts.enabled", False)

    if env_config.HEADLESS:
        options.add_argument("--headless=new")

    return options


def get_worker_id() -> str:
    """Get worker ID for xdist or fallback to local PID."""
    return os.environ.get("PYTEST_XDIST_WORKER") or "local"


def get_config_path(request: FixtureRequest, attr: str, error_msg: str) -> Path:
    value = getattr(request.config, attr, None)
    if value is None:
        raise RuntimeError(error_msg)
    return Path(value)


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
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{test_name.replace(':', '_').replace('/', '_')}.png"
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


# ============================================================================
# PYTEST FIXTURES
# ============================================================================


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    """
    Makes the root logger accessible to other files.
    """
    return root_logger


@pytest.fixture(scope="session", autouse=True)
def unique_user_data_dir(request: FixtureRequest) -> Generator[None, None, None]:
    """
    Creates and yields a unique Chrome user data directory per test.
    Ensures isolation between parallel test runs (xdist) by using worker ID or PID.
    Directory is created in system temp and stored in config for driver setup.
    """
    try:
        worker_id = request.config.workerinput.get("workerid")  # type: ignore[attr-defined]
    except Exception:
        worker_id = get_worker_id()

    user_data_dir = Path(tempfile.gettempdir()) / f"user_data_{worker_id}_{request.node.name}"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    request.config.user_data_dir = user_data_dir  # type: ignore[attr-defined]
    yield


@pytest.fixture(scope="session", autouse=True)
def clean_directories_at_start(request: FixtureRequest) -> None:
    """Clean screenshots, videos, and downloads directories at session start."""
    worker_id = get_worker_id()

    # Clean screenshots
    screenshots_dir = Path("tests_screenshots") / worker_id
    clean_directory(screenshots_dir, worker_id)

    # Clean videos
    videos_dir = Path("tests_recordings") / worker_id
    clean_directory(videos_dir, worker_id)

    # Clean downloads and store path in config
    downloads_dir = Path("downloads") / worker_id
    clean_directory(downloads_dir, worker_id)
    request.config.downloads_directory = downloads_dir  # type: ignore[attr-defined]


@pytest.fixture(scope="session")
def driver(request: FixtureRequest) -> Generator[WebDriver, None, None]:
    """Initialize driver object at the start of each test."""
    browser = request.config.getoption("--browser", default=env_config.BROWSER.lower())
    root_logger.debug(f"Initializing driver for browser: {browser} (Config: {env_config.BROWSER.lower()}).")

    downloads_directory = get_config_path(
        request, "downloads_directory", "downloads_directory not set by clean_downloads_per_test fixture."
    )
    user_data_dir = get_config_path(request, "user_data_dir", "user_data_dir not set by unique_user_data_dir fixture.")

    worker_token = os.environ.get("PYTEST_XDIST_WORKER", str(os.getpid()))
    port_suffix = int("".join(ch for ch in worker_token if ch.isdigit()) or "0") % 1000
    debug_port = DEBUG_PORT_BASE + port_suffix

    driver: WebDriver | None = None

    try:
        if browser == "chrome":
            chrome_driver_path = get_chrome_driver_path()
            chrome_service = ChromeService(chrome_driver_path)
            chrome_options = build_chrome_options(user_data_dir, downloads_directory, debug_port)
            driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

            # Set geolocation override after driver initialization
            driver.execute_cdp_cmd(
                "Browser.grantPermissions",
                {"origin": "https://the-internet.herokuapp.com", "permissions": ["geolocation"]},
            )
            driver.execute_cdp_cmd(
                "Emulation.setGeolocationOverride",
                {
                    "latitude": conftest_config.geolocation_lat,
                    "longitude": conftest_config.geolocation_lon,
                    "accuracy": 100,
                },
            )

        elif browser == "firefox":
            firefox_driver_path = get_firefox_driver_path()
            firefox_service = FirefoxService(firefox_driver_path)
            firefox_options = build_firefox_options(user_data_dir, downloads_directory)
            driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

            driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
            if env_config.MAXIMIZED:
                driver.maximize_window()

        else:
            raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'firefox'.")

        if driver is not None:
            try:
                driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
            except Exception:
                pass

        yield driver

    except Exception as e:
        root_logger.error(f"Failed to initialize {browser} driver: {str(e)}")
        raise
    finally:
        if driver is not None:
            root_logger.info(f"Quitting driver for browser: {browser}.")
            try:
                driver.quit()
            except Exception as e:
                root_logger.warning(f"Failed to quit driver: {str(e)}")


@pytest.fixture(scope="function")
def page_manager(driver: WebDriver, logger: Logger) -> PageManager:
    """
    Initialize PageManager object with driver and logger.
    """
    return PageManager(driver, logger)


@pytest.fixture(scope="function", autouse=True)
def test_setup(page_manager: PageManager, request: FixtureRequest) -> Generator[None, None, None]:
    """Set test context and navigate to base URL for UI tests."""
    test_name = request.node.name
    set_current_test(test_name)
    root_logger.info(f"Starting test: {test_name}")

    # Navigate to base URL for UI tests
    if request.node.get_closest_marker("ui") or request.node.get_closest_marker("current"):
        with allure.step(f"Navigate to base URL: {env_config.BASE_URL}"):
            page_manager.navigate_to_base_url(env_config.BASE_URL)

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

    worker_id = get_worker_id()
    test_name = request.node.name.replace(":", "_").replace("/", "_")

    stop_func, video_path = start_video_recording(driver, test_name, worker_id)
    root_logger.info(f"Started recording: {video_path}")

    try:
        yield
    finally:
        try:
            root_logger.info("Stopping video recording...")
            stop_func()

            # Wait briefly to ensure video is fully written
            import time

            time.sleep(1.0)

            # Attach video to test body
            video_path_obj = Path(video_path)
            if video_path_obj.exists() and video_path_obj.stat().st_size > 0:
                try:
                    lock_file = video_path_obj.parent / f"{worker_id}.lock"
                    with FileLock(lock_file):
                        allure.attach.file(
                            str(video_path_obj),
                            name="Test Recording",
                            attachment_type=allure.attachment_type.MP4,
                        )
                        root_logger.info(f"Video attached to test body: {video_path_obj}")
                except Exception as e:
                    root_logger.error(f"Failed to attach video: {str(e)}")
            else:
                root_logger.warning(f"Video file not found or empty: {video_path_obj}")
        except Exception as e:
            root_logger.error(f"Failed to stop video recording: {str(e)}")


@pytest.fixture(scope="function")
def actions(driver: WebDriver) -> ActionChains:
    """
    Provides a fresh ActionChains instance for the current WebDriver.
    Used for performing complex user interactions like drag-and-drop, right-click, etc.
    """
    return ActionChains(driver)


@pytest.fixture(scope="function")
def downloads_directory(request: FixtureRequest) -> Generator[Path, None, None]:
    """Provides clean downloads directory for tests marked with @pytest.mark.clean_downloads."""
    worker_id = get_worker_id()
    downloads_dir = Path("downloads") / worker_id

    # Only clean if test is marked
    if request.node.get_closest_marker("clean_downloads"):
        clean_directory(downloads_dir, worker_id)

    yield downloads_dir

    # Clean after test if marked
    if request.node.get_closest_marker("clean_downloads"):
        try:
            clean_directory(downloads_dir, worker_id)
            root_logger.info(f"Cleaned downloads after test: {request.node.name}")
        except Exception as e:
            root_logger.warning(f"Failed to clean downloads: {str(e)}")


# ============================================================================
# PYTEST HOOKS
# ============================================================================


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Add browser info to Allure environment and ensure clean results directory."""
    # Set geolocation values
    conftest_config.geolocation_lat = 32.0853
    conftest_config.geolocation_lon = 34.7818

    browser = config.getoption("--browser", default=env_config.BROWSER.lower())

    # Get the allure results directory from pytest options
    allure_results_dir = getattr(config.option, "allure_report_dir", None)

    if not allure_results_dir:
        # Fallback to default if not specified
        allure_results_dir = str(Path("reports") / "allure-results")
        config.option.allure_report_dir = allure_results_dir

    allure_results_path = Path(allure_results_dir)

    # Clean allure results ONLY for non-xdist runs to avoid mixing browser results
    if not os.environ.get("PYTEST_XDIST_WORKER"):
        if allure_results_path.exists():
            root_logger.info(f"Cleaning Allure results directory: {allure_results_path}")
            shutil.rmtree(allure_results_path, ignore_errors=True)

        # Create fresh directory
        allure_results_path.mkdir(parents=True, exist_ok=True)
        root_logger.info(f"Created fresh Allure results directory: {allure_results_path}")

        env_properties_path = allure_results_path / "environment.properties"
        with open(env_properties_path, "w") as f:
            f.write(f"Browser={browser.capitalize()}\n")
            f.write(f"Headless={env_config.HEADLESS}\n")
            f.write(f"Maximized={env_config.MAXIMIZED}\n")
            f.write(f"Base.URL={env_config.BASE_URL}\n")
            f.write(f"Window.Size={WINDOW_WIDTH}x{WINDOW_HEIGHT}\n")
            if os.environ.get("GITHUB_ACTIONS"):
                f.write(f"Run.ID={os.environ.get('GITHUB_RUN_ID', 'N/A')}\n")
                f.write(f"Workflow={os.environ.get('GITHUB_WORKFLOW', 'N/A')}\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item) -> Generator[None, None, None]:
    """
    Pytest hook to handle:
        - Test duration logging.
        - Screenshot taking on test failure (Locally and to Allure Report).
    """
    outcome = yield
    report = outcome.get_result()  # type: ignore[attr-defined]

    if report.when == "call":
        test_name = item.name
        duration = report.duration if hasattr(report, "duration") else 0

        # Log outcome explicitly
        outcome_str = "PASSED" if report.passed else "FAILED" if report.failed else "SKIPPED"
        root_logger.info(f"Test {outcome_str}: {test_name} (Duration: {duration:.2f}s).")

        # Take screenshot only on failure and only if driver is available
        if report.failed:
            driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
            if driver:
                try:
                    save_screenshot_on_failure(driver, test_name)
                except Exception as e:
                    root_logger.error(f"Failed to save screenshot for {test_name}: {str(e)}")

    elif report.when == "teardown":
        set_current_test(None)
        # Log teardown failures explicitly
        if report.failed:
            root_logger.error(f"Test teardown failed for: {item.name}")

        # Take screenshot only on failure and only if driver is available
        if report.failed:
            driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
            if driver:
                try:
                    save_screenshot_on_failure(driver, test_name)
                except Exception as e:
                    root_logger.error(f"Failed to save screenshot for {test_name}: {str(e)}")

    elif report.when == "teardown":
        set_current_test(None)
        # Log teardown failures explicitly
        if report.failed:
            root_logger.error(f"Test teardown failed for: {item.name}")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """
    Log final test session results.
    """
    passed = session.testscollected - session.testsfailed
    root_logger.info(
        f"Test session finished. Total: {session.testscollected}, "
        f"Passed: {passed}, Failed: {session.testsfailed}, "
        f"Exit status: {exitstatus}"
    )

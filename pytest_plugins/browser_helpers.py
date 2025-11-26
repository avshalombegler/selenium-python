"""Helper functions for browser driver setup and configuration."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.firefox import GeckoDriverManager

import config.env_config as env_config
from conftest import CACHE_VALID_RANGE, root_logger


def get_chrome_driver_path() -> str:
    """Get ChromeDriver path with extended cache and error handling."""
    # First try system chromedriver (Jenkins environment)
    system_path = shutil.which("chromedriver")
    if system_path:
        root_logger.info(f"Using system ChromeDriver: {system_path}")
        return system_path

    # Fallback to webdriver-manager for local development
    try:
        cache_manager = DriverCacheManager(valid_range=CACHE_VALID_RANGE)
        return ChromeDriverManager(cache_manager=cache_manager).install()
    except Exception as e:
        root_logger.error(f"Failed to download ChromeDriver: {e}")
        raise RuntimeError("ChromeDriver not found. Install manually or check GitHub API limits.")


def get_firefox_driver_path() -> str:
    """Get GeckoDriver path with extended cache and error handling."""
    # First try system geckodriver (Jenkins environment)
    system_path = shutil.which("geckodriver")
    if system_path:
        root_logger.info(f"Using system GeckoDriver: {system_path}")
        return system_path

    # Fallback to webdriver-manager for local development
    try:
        cache_manager = DriverCacheManager(valid_range=CACHE_VALID_RANGE)
        return GeckoDriverManager(cache_manager=cache_manager).install()
    except Exception as e:
        root_logger.error(f"Failed to download GeckoDriver: {e}")
        raise RuntimeError("GeckoDriver not found. Install manually or check GitHub API limits.")


def build_chrome_options(user_data_dir: Path, downloads_directory: Path, debug_port: int) -> ChromeOptions:
    """Build Chrome options with all necessary configurations."""
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
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "autofill.profile_enabled": False,
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
    """Build Firefox options with all necessary configurations."""
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
    profile.set_preference("geo.provider.testing", False)

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

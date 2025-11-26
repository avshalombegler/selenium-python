"""Browser driver and action chain fixtures."""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service as FirefoxService

import config.conftest_config as conftest_config
import config.env_config as env_config
from conftest import DEBUG_PORT_BASE, WINDOW_HEIGHT, WINDOW_WIDTH, root_logger
from pytest_plugins.browser_helpers import (
    build_chrome_options,
    build_firefox_options,
    get_chrome_driver_path,
    get_firefox_driver_path,
)

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from selenium.webdriver.remote.webdriver import WebDriver


def get_config_path(request: FixtureRequest, attr: str, error_msg: str) -> Path:
    """Get path from pytest config with error handling."""
    value = getattr(request.config, attr, None)
    if value is None:
        raise RuntimeError(error_msg)
    return Path(value)


@pytest.fixture(scope="session")
def driver(request: FixtureRequest) -> Generator[WebDriver, None, None]:
    """Initialize driver object at the start of each test."""
    # Use browser value set by pytest_configure hook
    browser = getattr(request.config, "browser", env_config.BROWSER.lower())
    root_logger.debug(f"Initializing driver for browser: {browser}.")

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
def actions(driver: WebDriver) -> ActionChains:
    """
    Provides a fresh ActionChains instance for the current WebDriver.
    Used for performing complex user interactions like drag-and-drop, right-click, etc.
    """
    return ActionChains(driver)

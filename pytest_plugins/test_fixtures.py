"""Test setup and page manager fixtures."""

from __future__ import annotations

import logging
from collections.abc import Generator
from typing import TYPE_CHECKING

import allure
import pytest

import config.env_config as env_config
from conftest import root_logger
from pages.base.page_manager import PageManager
from utils.logging_helper import set_current_test

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from selenium.webdriver.remote.webdriver import WebDriver


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    """
    Makes the root logger accessible to other files.
    """
    return root_logger


@pytest.fixture(scope="function")
def page_manager(driver: WebDriver, logger: logging.Logger) -> PageManager:
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

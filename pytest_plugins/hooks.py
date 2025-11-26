"""Pytest hooks for test lifecycle management."""

from __future__ import annotations

import os
import shutil
from collections.abc import Generator
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import allure
import pytest
from _pytest.main import Session
from _pytest.nodes import Item
from filelock import FileLock

import config.conftest_config as conftest_config
import config.env_config as env_config
from conftest import WINDOW_HEIGHT, WINDOW_WIDTH, root_logger
from pytest_plugins.browser_helpers import get_worker_id
from utils.logging_helper import set_current_test

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


def save_screenshot_on_failure(driver: WebDriver, test_name: str) -> None:
    """Capture and save screenshot on test failure."""
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


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default=None,  # Will fallback to env_config.BROWSER
        help="Browser to run tests: chrome or firefox",
        choices=["chrome", "firefox"],
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Add browser info to Allure environment and ensure clean results directory."""
    # Set geolocation values
    conftest_config.geolocation_lat = 32.0853
    conftest_config.geolocation_lon = 34.7818

    # Get browser from CLI arg, then env var, then config default
    browser = config.getoption("--browser", default=None)
    if browser is None:
        browser = os.environ.get("BROWSER", env_config.BROWSER).lower()
    else:
        browser = browser.lower()

    # Store for use in fixtures
    config.browser = browser  # type: ignore[attr-defined]

    # Get the allure results directory from pytest options
    allure_results_dir = getattr(config.option, "allure_report_dir", None)

    if not allure_results_dir:
        # Fallback to default if not specified
        allure_results_dir = str(Path("reports") / "allure-results")
        config.option.allure_report_dir = allure_results_dir

    allure_results_path = Path(allure_results_dir)

    # Clean allure results ONLY for non-xdist runs and local development
    # Don't clean in CI environments (Jenkins or GitHub Actions) where browsers run in parallel
    is_ci_environment = os.environ.get("JENKINS_HOME") or os.environ.get("GITHUB_ACTIONS")
    is_xdist_worker = os.environ.get("PYTEST_XDIST_WORKER")

    if not is_xdist_worker and not is_ci_environment:
        if allure_results_path.exists():
            root_logger.info(f"Cleaning Allure results directory: {allure_results_path}")
            shutil.rmtree(allure_results_path, ignore_errors=True)

        # Create fresh directory
        allure_results_path.mkdir(parents=True, exist_ok=True)
        root_logger.info(f"Created fresh Allure results directory: {allure_results_path}")
    else:
        # In CI or xdist, just ensure directory exists
        allure_results_path.mkdir(parents=True, exist_ok=True)
        if is_ci_environment:
            root_logger.info(f"Running in CI environment - preserving existing results in: {allure_results_path}")

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
        elif os.environ.get("JENKINS_HOME"):
            f.write(f"Build.Number={os.environ.get('BUILD_NUMBER', 'N/A')}\n")
            f.write(f"Job.Name={os.environ.get('JOB_NAME', 'N/A')}\n")


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
            # Take screenshot on teardown failure
            driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
            if driver:
                try:
                    save_screenshot_on_failure(driver, item.name)
                except Exception as e:
                    root_logger.error(f"Failed to save screenshot for {item.name}: {str(e)}")


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

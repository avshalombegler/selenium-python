"""Video recording fixtures."""

from __future__ import annotations

import time
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING

import allure
import pytest
from filelock import FileLock

import config.env_config as env_config
from conftest import root_logger
from pytest_plugins.browser_helpers import get_worker_id
from utils.video_recorder import start_video_recording

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from selenium.webdriver.remote.webdriver import WebDriver


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

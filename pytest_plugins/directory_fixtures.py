"""Directory management fixtures for screenshots, videos, and downloads."""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from filelock import FileLock

from conftest import root_logger
from pytest_plugins.browser_helpers import get_worker_id

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest


def clean_directory(dir_path: Path, lock_suffix: str = "lock") -> None:
    """Helper to clean and recreate a directory with file locking."""
    lock_file = dir_path / f"{lock_suffix}.lock"
    dir_path.mkdir(parents=True, exist_ok=True)
    with FileLock(lock_file):
        if dir_path.exists():
            shutil.rmtree(dir_path, ignore_errors=True)
        dir_path.mkdir(parents=True, exist_ok=True)
        root_logger.info(f"Directory cleaned and recreated at: {dir_path}.")


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

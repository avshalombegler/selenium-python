"""Main conftest - registers plugins and exposes fixtures."""

from __future__ import annotations

import logging

from utils.logging_helper import configure_root_logger

# Register plugin modules
pytest_plugins = [
    "pytest_plugins.browser_fixtures",
    "pytest_plugins.directory_fixtures",
    "pytest_plugins.test_fixtures",
    "pytest_plugins.recording_fixtures",
    "pytest_plugins.hooks",
]

# Constants shared across plugins

DEBUG_PORT_BASE = 9222
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
CACHE_VALID_RANGE = 30

# Configure root logger once for the test session
root_logger = configure_root_logger(log_file="test_logs.log", level=logging.INFO)

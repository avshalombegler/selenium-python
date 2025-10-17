import logging
from contextvars import ContextVar
from typing import Optional

# Context variable that holds the current test name for the running context
current_test_name: ContextVar[str] = ContextVar("current_test_name", default="")


class TestNameFilter(logging.Filter):
    """
    Logging filter that injects the current test name into LogRecord as `test_name`.

    This avoids KeyError when format strings reference %(test_name)s and works with
    pytest and threaded/async code because it uses ContextVar.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.test_name = current_test_name.get()
        return True


def configure_root_logger(log_file: str = "test_logs.log", level: int = logging.INFO) -> logging.Logger:
    """
    Configure the root logger with a file and stream handler and attach TestNameFilter.

    Returns the root logger instance.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # Clear existing handlers to avoid duplicate logs when reconfiguring
    logger.handlers = []

    # Use a SafeFormatter to avoid KeyError when third-party libraries log with
    # different/bare format keys. It fills missing keys with an empty string.
    class SafeFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            if not hasattr(record, "test_name"):
                record.test_name = ""
            try:
                return super().format(record)
            except KeyError:
                # Fallback: ensure record has message-like attributes
                record.test_name = getattr(record, "test_name", "")
                record.msg = getattr(record, "msg", "")
                return super().format(record)

    formatter = SafeFormatter("%(asctime)s - %(levelname)s - [%(test_name)s] %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(TestNameFilter())

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(TestNameFilter())

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def set_current_test(name: Optional[str]):
    """
    Set the current test name for logging. Pass None or empty string to clear.
    """
    if name:
        current_test_name.set(name)
    else:
        current_test_name.set("")


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a configured logger.

    If the root logger has not been configured yet (no handlers), call
    configure_root_logger() with defaults so tests and pages can safely
    obtain a session/root logger without importing conftest.

    If `name` is provided, returns a child logger with that name, otherwise
    returns the root logger instance.
    """
    root = logging.getLogger()
    if not root.handlers:
        # Configure with defaults if not already configured elsewhere
        configure_root_logger()
    return logging.getLogger(name) if name else root

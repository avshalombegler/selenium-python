from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple, TypeVar, Union, List, cast
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    JavascriptException,
)
from logging import Logger
from utils.logging_helper import get_logger
from config.env_config import SHORT_TIMEOUT, LONG_TIMEOUT, BASE_URL

# === TYPE CHECKING ONLY ===
if TYPE_CHECKING:
    # Use simple string-based locators for typing so they match selenium expected_conditions signatures
    from selenium.webdriver.common.by import By  # noqa: F401 (only for dev clarity)
    from pages.base.page_manager import PageManager

    Locator = Tuple[str, str]
else:
    from selenium.webdriver.support import expected_conditions as EC

    Locator = Any

# When not TYPE_CHECKING we still need EC available for runtime
if TYPE_CHECKING:
    from selenium.webdriver.support import expected_conditions as EC
else:
    # already imported above in else block
    pass

# Generic return type – usually WebElement or bool
T = TypeVar("T")


class BasePage:
    def __init__(self, driver: WebDriver, logger: Logger | None = None) -> None:
        self.driver = driver
        # Accept an injected logger (for tests) or use a sensible default from logging_helper
        self.logger = logger if logger is not None else get_logger(self.__class__.__name__)
        self.short_wait = SHORT_TIMEOUT
        self.long_wait = LONG_TIMEOUT
        self.base_url = BASE_URL

    def _safe_wait(
        self,
        ec_method: Callable[..., Callable[[Any], T]],
        locator: Any,
        timeout: Optional[Union[int, float]] = None,
    ) -> T:
        """
        Generic wait with exception handling.

        Args:
            ec_method: Expected condition method (e.g., EC.visibility_of_element_located)
            locator: Tuple of (By, "selector")
            timeout: Wait timeout in seconds (defaults to self.short_wait)

        Returns:
            Result of the expected condition (usually WebElement or bool)

        Raises:
            TimeoutException: If condition not met
            NoSuchElementException: If element not found
            Exception: For any other error
        """
        timeout = timeout or self.short_wait
        wait = WebDriverWait(self.driver, timeout)
        try:
            # ec_method may be a function like EC.visibility_of_element_located or
            # EC.invisibility_of_element (when given a WebElement)
            try:
                name = getattr(ec_method, "__name__", repr(ec_method))
            except Exception:
                name = repr(ec_method)
            self.logger.debug(f"Waiting for {name} on locator {locator} with timeout {timeout}s.")
            return wait.until(ec_method(locator))
        except TimeoutException as e:
            self.logger.error(f"Timeout after {timeout}s for locator {locator}: {str(e)}")
            raise  # Let pytest hook handle screenshot
        except NoSuchElementException as e:
            self.logger.error(f"No element found for locator {locator}: {str(e)}")
            raise
        except Exception as e:  # Catch-all for unexpected
            self.logger.critical(f"Unexpected error for locator {locator}: {str(e)}")
            raise

    def _retry(
        self,
        func: Callable[[], Any],
        locator: Locator | None = None,
        retry_count: int = 2,
        exceptions: tuple[type[BaseException], ...] = (Exception,),
        final_message: str | None = None,
    ) -> Any:
        """
        Generic retry helper used to reduce duplicate retry loops.
        - func: callable to execute
        - locator: used only for logging context
        - retry_count: attempts
        - exceptions: tuple of exceptions to catch and retry on
        - final_message: optional final error message to log before re-raising
        """
        for attempt in range(retry_count):
            try:
                return func()
            except exceptions as e:
                self.logger.warning(f"Attempt {attempt+1}/{retry_count} failed for {locator}: {str(e)}")
                if attempt == retry_count - 1:
                    msg = final_message or f"All retries failed for {locator}"
                    self.logger.error(msg)
                    raise

    def wait_for_page_to_load(self, indicator_locator: Locator, timeout: Optional[Union[int, float]] = None) -> None:
        """
        Wait for page to load by checking visibility of an indicator element.

        Args:
            indicator_locator: Tuple of (By, value) for the indicator element.
            timeout: Optional timeout in seconds (defaults to LONG_TIMEOUT).

        Raises:
            TimeoutException: If the indicator is not visible within timeout.
            NoSuchElementException: If the locator is invalid.
        """
        timeout = timeout or self.long_wait
        wait = WebDriverWait(self.driver, timeout)
        try:
            self.logger.info(f"Waiting for page to load with indicator '{indicator_locator}' for {timeout}s.")
            wait.until(
                EC.visibility_of_element_located(indicator_locator),
                message=f"Page load failed: indicator '{indicator_locator}' not visible after {timeout}s",
            )
            self.logger.info(f"Page loaded successfully with indicator '{indicator_locator}'.")
        except TimeoutException as e:
            self.logger.error(f"Page load timed out after {timeout}s for indicator '{indicator_locator}': {str(e)}")
            raise  # Let hook handle screenshot
        except NoSuchElementException as e:
            self.logger.error(f"Invalid locator '{indicator_locator}': {str(e)}")
            raise

    def wait_for_visibility(self, locator: Locator, timeout: Optional[Union[int, float]] = None) -> "WebElement":
        """Wait for element visible"""
        return cast(WebElement, self._safe_wait(EC.visibility_of_element_located, locator, timeout))

    def wait_for_invisibility(self, locator: Locator, timeout: Optional[Union[int, float]] = None) -> bool:
        """Wait for element invisible (use EC that accepts WebElement)"""
        timeout = timeout or self.short_wait
        elem = self.wait_for_visibility(locator, timeout)
        wait = WebDriverWait(self.driver, timeout)
        # invisibility_of_element expects a WebElement; ensure bool return for mypy
        result = wait.until(EC.invisibility_of_element(elem))
        return bool(result)

    def wait_for_loader(self, locator: Locator, timeout: Optional[Union[int, float]] = None) -> bool:
        """
        Wait for loading indicator to appear and disappear.
        Returns True if loader completed normally, False if timeout occurred.
        """
        timeout = timeout or self.long_wait
        self.logger.info("Waiting for loader to disappear.")
        try:
            # Split timeout between appearing and disappearing
            half_timeout = max(timeout / 2, 1)  # At least 1 second each
            self.wait_for_visibility(locator, timeout=half_timeout)
            self.wait_for_invisibility(locator, timeout=half_timeout)
            return True
        except TimeoutException as e:
            self.logger.warning(f"Loader timeout after {timeout}s: {str(e)}")
            return False

    def navigate_to(self, url: str) -> None:
        self.logger.info(f"Navigating to URL: {url}.")
        self.driver.get(url)
        self.logger.info("Navigation completed.")

    def click_element(self, locator: Locator, retry: int = 2) -> None:
        """Click with retry for stale/intercepted, no screenshot"""

        def action() -> None:
            elem = self.wait_for_visibility(locator)
            self._safe_wait(EC.element_to_be_clickable, locator)
            elem.click()
            self.logger.debug(f"Clicked on element with locator '{locator}'.")

        # Call _retry but do not return its Any to satisfy a None return type
        self._retry(action, locator=locator, retry_count=retry)
        return None

    def get_dynamic_element_text(
        self, locator: Locator, timeout: Optional[Union[int, float]] = None, retry: int = 2
    ) -> str:
        """
        Get text with retry for stale elements.

        Args:
            locator: Tuple of (By, value) for the element.
            timeout: Optional timeout in seconds (defaults to LONG_TIMEOUT).
            retry_count: Number of retry attempts for stale elements.

        Returns:
            str: Text of the element.

        Raises:
            TimeoutException: If element is not visible within timeout.
            NoSuchElementException: If element cannot be found after retries.
        """
        timeout = timeout or self.long_wait

        def action() -> str | Any:
            self.logger.debug(f"Waiting for '{locator}' visibility.")
            elem = self.wait_for_visibility(locator, timeout)
            text = elem.text
            self.logger.debug(f"Retrieved text: '{text}'.")
            return text

        # Only retry on stale element; other exceptions should propagate immediately
        return self._retry(
            action,
            locator=locator,
            retry_count=retry,
            exceptions=(StaleElementReferenceException,),
            final_message=f"Failed to get text for '{locator}' after {retry} attempts",
        )

    def get_number_of_elements(self, locator: Locator) -> int:
        self.logger.info(f"Counting elements with locator: '{locator}'.")
        try:
            elements = WebDriverWait(self.driver, self.short_wait).until(
                EC.presence_of_all_elements_located(locator),
                message=f"Timeout waiting for elements with locator '{locator}'.",
            )
            count = len(elements)
            self.logger.debug(f"Found {count} elements with locator '{locator}'.")
            return count
        except TimeoutException:
            self.logger.debug(f"No elements found with locator '{locator}' after {SHORT_TIMEOUT}s, returning 0.")
            return 0

    def get_all_elements(self, locator: Locator) -> List[WebElement]:
        try:
            elements = WebDriverWait(self.driver, self.short_wait).until(
                EC.presence_of_all_elements_located(locator),
                message=f"Timeout waiting for elements with locator '{locator}'",
            )
            return elements
        except TimeoutException:
            self.logger.debug(f"No elements found with locator {locator} after {SHORT_TIMEOUT}s.")
        return []

    def get_element_attr_js(self, web_element: WebElement, attr: str) -> Any | None:
        """
        Get element attribute using JavaScript execution.

        Args:
            web_element: WebElement to get attribute from
            attr: Attribute name to retrieve

        Returns:
            Any: Attribute value or None if execution failed

        Raises:
            JavascriptException: If script execution fails
        """
        try:
            result = self.driver.execute_script(f"return arguments[0].{attr}", web_element)
            self.logger.debug(f"Retrieved {attr}={result} for element.")
            return result
        except JavascriptException as e:
            self.logger.error(f"Failed to get {attr}: {str(e)}")
            return None

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_base_url(self) -> str:
        return self.base_url

    def get_files_in_directory(self, directory_path: Path) -> list:
        """
        Returns a list of file names in the specified directory.
        """
        return [item for item in directory_path.iterdir() if item.is_file()]

    def is_element_selected(
        self, locator: Locator, timeout: Optional[Union[int, float]] = None, retry: int = 2
    ) -> bool:
        self.logger.info(f"Check element with locator '{locator}' selected state.")

        def action() -> bool | Any:
            elem = self.wait_for_visibility(locator, timeout)
            state = elem.is_selected()
            self.logger.debug(f"Element with locator '{locator}' selected state '{state}'.")
            return state

        return self._retry(action, locator=locator, retry_count=retry)

    def is_element_enabled(self, locator: Locator, timeout: Optional[Union[int, float]] = None, retry: int = 2) -> bool:
        self.logger.info(f"Check element with locator '{locator}' enabled state.")

        def action() -> bool | Any:
            elem = self.wait_for_visibility(locator, timeout)
            state = elem.is_enabled()
            self.logger.debug(f"Element with locator '{locator}' enabled state '{state}'.")
            return state

        return self._retry(action, locator=locator, retry_count=retry)

    def is_element_visible(self, locator: Locator, timeout: Optional[Union[int, float]] = None) -> bool:
        """Check if element is visible (in DOM + displayed)"""
        try:
            self._safe_wait(EC.visibility_of_element_located, locator, timeout)
            return True
        except TimeoutException:
            return False

    def perform_right_click(self, locator: Locator, actions: ActionChains, retry: int = 2) -> None:
        self.logger.info(f"Performing right-click on element with locator '{locator}'.")

        def action() -> None:
            elem = self.wait_for_visibility(locator)
            actions.context_click(elem).perform()
            self.logger.debug(f"Performed right-click on element '{elem}'.")

        self._retry(action, locator=locator, retry_count=retry)
        return None

    def refresh_page(self) -> None:
        return self.driver.refresh()

    def send_keys_to_element(self, locator: Locator, text: str, retry: int = 2) -> None:
        self.logger.info(f"Send keys '{text}' to element with locator '{locator}'.")

        def action() -> None:
            elem = self.wait_for_visibility(locator)
            elem.send_keys(text)

        self._retry(action, locator=locator, retry_count=retry)
        return None

    def download_file(self, locator: Locator, file_name: str, retry: int = 2) -> None:
        self.logger.info(f"Download file '{file_name}'.")

        formatted_locaor = (locator[0], locator[1].format(file_name=file_name))

        def action() -> None:
            link_element = self.wait_for_visibility(formatted_locaor)
            if link_element:
                self.click_element(formatted_locaor)
                self.logger.info(f"Clicked download link for file: {file_name}")
            else:
                raise ValueError(f"Download link for file '{file_name}' not found.")

        self._retry(action, locator=locator, retry_count=retry)
        return None

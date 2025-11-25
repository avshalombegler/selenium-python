from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple, TypeVar, Union, List, cast
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    JavascriptException,
)
from logging import Logger
from utils.logging_helper import get_logger
from config.env_config import SHORT_TIMEOUT, LONG_TIMEOUT, BASE_URL

if TYPE_CHECKING:
    Locator = Tuple[str, str]
else:
    Locator = Any

T = TypeVar("T")


class BasePage:
    """
    Base page object providing common web automation methods.

    Method Categories:
    1. Initialization
    2. Core Helpers (Private)
    3. Wait Methods
    4. Navigation Methods
    5. Element Interaction Methods
    6. Element State Methods
    7. Element Query Methods
    8. Utility Methods
    """

    # ============================================================================
    # INITIALIZATION
    # ============================================================================

    def __init__(self, driver: WebDriver, logger: Logger | None = None) -> None:
        self.driver = driver
        self.logger = logger if logger is not None else get_logger(self.__class__.__name__)
        self.short_wait = SHORT_TIMEOUT
        self.long_wait = LONG_TIMEOUT
        self.base_url = BASE_URL

    # ============================================================================
    # CORE HELPERS (PRIVATE)
    # ============================================================================

    def _get_timeout(self, timeout: Optional[Union[int, float]], use_long: bool = False) -> Union[int, float]:
        """
        Centralized timeout resolution.

        Args:
            timeout: Explicit timeout value or None
            use_long: If True and timeout is None, use long_wait instead of short_wait

        Returns:
            Resolved timeout value
        """
        if timeout is not None:
            return timeout
        return self.long_wait if use_long else self.short_wait

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
        timeout = self._get_timeout(timeout)
        wait = WebDriverWait(self.driver, timeout)
        try:
            try:
                name = getattr(ec_method, "__name__", repr(ec_method))
            except Exception:
                name = repr(ec_method)
            self.logger.debug(f"Waiting for {name} on locator {locator} with timeout {timeout}s.")
            return wait.until(ec_method(locator))
        except TimeoutException as e:
            self.logger.error(f"Timeout after {timeout}s for locator {locator}: {str(e)}")
            raise
        except NoSuchElementException as e:
            self.logger.error(f"No element found for locator {locator}: {str(e)}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error for locator {locator}: {str(e)}")
            raise

    def _execute_element_action(
        self,
        locator: Locator,
        action_name: str,
        action_func: Callable[[WebElement], Any],
        timeout: Optional[Union[int, float]] = None,
        retry: int = 2,
    ) -> Any:
        """
        Generic method for element actions with retry.

        Args:
            locator: Element locator tuple
            action_name: Description of action for logging (e.g., "Check enabled state")
            action_func: Function to execute on the WebElement
            timeout: Optional timeout for waiting
            retry: Number of retry attempts

        Returns:
            Result of action_func
        """
        self.logger.info(f"{action_name} on element '{locator}'.")

        def action() -> Any:
            elem = self.wait_for_visibility(locator, timeout)
            result = action_func(elem)
            self.logger.debug(f"{action_name} completed for '{locator}'.")
            return result

        return self._retry(action, locator=locator, retry_count=retry)

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

        Args:
            func: Callable to execute
            locator: Used only for logging context
            retry_count: Number of attempts
            exceptions: Tuple of exceptions to catch and retry on
            final_message: Optional final error message to log before re-raising

        Returns:
            Result of func()

        Raises:
            Last exception encountered after all retries exhausted
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

    # ============================================================================
    # WAIT METHODS
    # ============================================================================

    def wait_for_page_to_load(self, indicator_locator: Locator, timeout: Optional[Union[int, float]] = None) -> None:
        """
        Wait for page to load by checking visibility of an indicator element.

        Args:
            indicator_locator: Tuple of (By, value) for the indicator element
            timeout: Optional timeout in seconds (defaults to LONG_TIMEOUT)

        Raises:
            TimeoutException: If the indicator is not visible within timeout
            NoSuchElementException: If the locator is invalid
        """
        timeout = self._get_timeout(timeout, use_long=True)
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
            raise
        except NoSuchElementException as e:
            self.logger.error(f"Invalid locator '{indicator_locator}': {str(e)}")
            raise

    def wait_for_visibility(self, locator: Locator, timeout: Optional[Union[int, float]] = None) -> WebElement:
        """
        Wait for element to be visible.

        Args:
            locator: Element locator tuple
            timeout: Optional timeout in seconds

        Returns:
            WebElement: The visible element

        Raises:
            TimeoutException: If element not visible within timeout
        """
        return cast(WebElement, self._safe_wait(EC.visibility_of_element_located, locator, timeout))

    def wait_for_invisibility(self, locator: Locator, timeout: Optional[Union[int, float]] = None) -> bool:
        """
        Wait for element to become invisible.

        Args:
            locator: Element locator tuple
            timeout: Optional timeout in seconds

        Returns:
            bool: True if element became invisible

        Raises:
            TimeoutException: If element remains visible after timeout
        """
        timeout = self._get_timeout(timeout)
        elem = self.wait_for_visibility(locator, timeout)
        wait = WebDriverWait(self.driver, timeout)
        result = wait.until(EC.invisibility_of_element(elem))
        return bool(result)

    def wait_for_loader(self, locator: Locator, timeout: Optional[Union[int, float]] = None) -> bool:
        """
        Wait for loading indicator to appear and disappear.

        Args:
            locator: Loader element locator tuple
            timeout: Optional timeout in seconds

        Returns:
            bool: True if loader completed, False if timeout
        """
        timeout = self._get_timeout(timeout)
        self.logger.info("Waiting for loader to complete.")

        try:
            half_timeout = timeout / 2
            self.wait_for_visibility(locator, timeout=half_timeout)
            self.wait_for_invisibility(locator, timeout=half_timeout)
            self.logger.debug("Loader completed successfully.")
            return True
        except TimeoutException as e:
            self.logger.warning(f"Loader timeout after {timeout}s: {str(e)}")
            return False

    # ============================================================================
    # NAVIGATION METHODS
    # ============================================================================

    def navigate_to(self, url: str) -> None:
        """
        Navigate to a URL.

        Args:
            url: Target URL to navigate to
        """
        self.logger.info(f"Navigating to URL: {url}.")
        self.driver.get(url)
        self.logger.info("Navigation completed.")

    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.logger.info("Refreshing page.")
        self.driver.refresh()
        self.logger.info("Page refreshed.")

    def navigate_back(self) -> None:
        """Navigate back."""
        self.logger.info("Navigating back.")
        self.driver.back()
        self.logger.info("Navigation completed.")

    # ============================================================================
    # FRAME/WINDOW METHODS
    # ============================================================================

    def switch_to_frame(self, locator: Locator, retry: int = 2) -> None:
        """
        Switch to an iframe or frame with retry.

        Args:
            locator: Frame element locator tuple
            retry: Number of retry attempts

        Raises:
            Exception: If frame switch fails after all retries
        """

        def action() -> None:
            try:
                elem = self.wait_for_visibility(locator)
                self.driver.switch_to.frame(elem)
                self.logger.debug(f"Switched to frame with locator '{locator}'.")
            except NoSuchElementException as e:
                self.logger.warning(f"Frame not found with locator '{locator}': {str(e)}")
                raise
            except StaleElementReferenceException as e:
                self.logger.warning(f"Frame element stale for '{locator}': {str(e)}")
                raise

        self._retry(action, locator=locator, retry_count=retry)

    # ============================================================================
    # ELEMENT INTERACTION METHODS
    # ============================================================================

    def click_element(self, locator: Locator, retry: int = 2) -> None:
        """
        Click an element with retry for stale/intercepted exceptions.

        Args:
            locator: Element locator tuple
            retry: Number of retry attempts

        Raises:
            Exception: If click fails after all retries
        """

        def action() -> None:
            elem = self.wait_for_visibility(locator)
            self._safe_wait(EC.element_to_be_clickable, locator)
            elem.click()
            self.logger.debug(f"Clicked on element with locator '{locator}'.")

        self._retry(action, locator=locator, retry_count=retry)

    def send_keys_to_element(self, locator: Locator, text: str, retry: int = 2) -> None:
        """
        Send keys to an element with retry.

        Args:
            locator: Element locator tuple
            text: Text to send to the element
            retry: Number of retry attempts

        Raises:
            Exception: If send keys fails after all retries
        """
        self._execute_element_action(
            locator,
            f"Sending keys '{text}'",
            lambda elem: elem.send_keys(text),
            retry=retry,
        )

    def perform_right_click(self, locator: Locator, actions: ActionChains, retry: int = 2) -> None:
        """
        Perform right-click on an element with retry.

        Args:
            locator: Element locator tuple
            actions: ActionChains instance for performing the action
            retry: Number of retry attempts

        Raises:
            Exception: If right-click fails after all retries
        """
        self._execute_element_action(
            locator,
            "Performing right-click",
            lambda elem: actions.context_click(elem).perform(),
            retry=retry,
        )

    def download_file(
        self, locator: Locator, file_name: str, timeout: Optional[Union[int, float]] = None, retry: int = 2
    ) -> None:
        """
        Click a download link for a specific file with retry.

        Args:
            locator: Download link locator with {file_name} placeholder
            file_name: Name of the file to download
            timeout: Optional timeout for waiting
            retry: Number of retry attempts

        Raises:
            Exception: If download click fails after all retries
        """
        self.logger.info(f"Downloading file '{file_name}'.")
        formatted_locator = (locator[0], locator[1].format(file_name=file_name))

        def action() -> None:
            self.wait_for_visibility(formatted_locator, timeout)
            self.click_element(formatted_locator)
            self.logger.debug(f"Clicked download link for file: {file_name}")

        self._retry(action, locator=formatted_locator, retry_count=retry)

    # ============================================================================
    # ELEMENT STATE METHODS
    # ============================================================================

    def is_element_visible(self, locator: Locator, timeout: Optional[Union[int, float]] = None) -> bool:
        """
        Check if element is visible (in DOM and displayed).

        Args:
            locator: Element locator tuple
            timeout: Optional timeout for waiting

        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            self._safe_wait(EC.visibility_of_element_located, locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_selected(
        self, locator: Locator, timeout: Optional[Union[int, float]] = None, retry: int = 2
    ) -> bool:
        """
        Check if element is selected (e.g., checkbox, radio button).

        Args:
            locator: Element locator tuple
            timeout: Optional timeout for waiting
            retry: Number of retry attempts

        Returns:
            bool: True if element is selected, False otherwise
        """
        return bool(
            self._execute_element_action(
                locator,
                "Checking selected state",
                lambda elem: elem.is_selected(),
                timeout,
                retry,
            )
        )

    def is_element_enabled(self, locator: Locator, timeout: Optional[Union[int, float]] = None, retry: int = 2) -> bool:
        """
        Check if element is enabled (not disabled).

        Args:
            locator: Element locator tuple
            timeout: Optional timeout for waiting
            retry: Number of retry attempts

        Returns:
            bool: True if element is enabled, False otherwise
        """
        return bool(
            self._execute_element_action(
                locator,
                "Checking enabled state",
                lambda elem: elem.is_enabled(),
                timeout,
                retry,
            )
        )

    # ============================================================================
    # ELEMENT QUERY METHODS
    # ============================================================================

    def get_dynamic_element_text(
        self, locator: Locator, timeout: Optional[Union[int, float]] = None, retry: int = 2
    ) -> str:
        """
        Get text from an element with retry for stale elements.

        Args:
            locator: Element locator tuple
            timeout: Optional timeout in seconds (defaults to LONG_TIMEOUT)
            retry: Number of retry attempts for stale elements

        Returns:
            str: Text content of the element

        Raises:
            TimeoutException: If element is not visible within timeout
            StaleElementReferenceException: If element cannot be found after retries
        """
        timeout = self._get_timeout(timeout, use_long=True)

        def action() -> str:
            self.logger.debug(f"Waiting for '{locator}' visibility.")
            elem = self.wait_for_visibility(locator, timeout)
            text = elem.text
            self.logger.debug(f"Retrieved text: '{text}'.")
            return text

        return self._retry(
            action,
            locator=locator,
            retry_count=retry,
            exceptions=(StaleElementReferenceException,),
            final_message=f"Failed to get text for '{locator}' after {retry} attempts",
        )

    def get_all_elements(self, locator: Locator) -> List[WebElement]:
        """
        Get all elements matching the locator.

        Args:
            locator: Element locator tuple

        Returns:
            List[WebElement]: List of matching elements (empty if none found)
        """
        try:
            elements = WebDriverWait(self.driver, self.short_wait).until(
                EC.presence_of_all_elements_located(locator),
                message=f"Timeout waiting for elements with locator '{locator}'",
            )
            return elements
        except TimeoutException:
            self.logger.debug(f"No elements found with locator {locator} after {SHORT_TIMEOUT}s.")
            return []

    def get_number_of_elements(self, locator: Locator) -> int:
        """
        Count the number of elements matching the locator.

        Args:
            locator: Element locator tuple

        Returns:
            int: Number of matching elements
        """
        self.logger.info(f"Counting elements with locator: '{locator}'.")
        elements = self.get_all_elements(locator)
        count = len(elements)
        self.logger.debug(f"Found {count} elements with locator '{locator}'.")
        return count

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
        """
        Get the current page URL.

        Returns:
            str: Current URL
        """
        url = self.driver.current_url
        self.logger.debug(f"Current URL: {url}")
        return url

    def get_base_url(self) -> str:
        """
        Get the base URL from configuration.

        Returns:
            str: Base URL
        """
        url = self.base_url
        self.logger.debug(f"Base URL: {url}")
        return url

    def get_page_source(self, timeout: Optional[Union[int, float]] = None, lowercase: bool = False) -> str:
        """
        Get the page source with optional wait for page readiness.

        Args:
            timeout: Optional timeout for waiting for document ready state
            lowercase: If True, return lowercase version of page source

        Returns:
            str: Page source HTML (optionally lowercased)

        Raises:
            TimeoutException: If page doesn't reach ready state within timeout
        """
        timeout = self._get_timeout(timeout, use_long=True)
        self.logger.info("Getting page source.")

        try:
            # Wait for document ready state
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda d: d.execute_script("return document.readyState") == "complete",
                message=f"Page not ready after {timeout}s",
            )

            page_source = self.driver.page_source

            if lowercase:
                page_source = page_source.lower()
                self.logger.debug("Retrieved page source (lowercased).")
            else:
                self.logger.debug("Retrieved page source.")

            return page_source

        except TimeoutException as e:
            self.logger.warning(f"Timeout waiting for page ready state: {str(e)}")
            # Return page source anyway even if not fully ready
            page_source = self.driver.page_source
            return page_source.lower() if lowercase else page_source
        except Exception as e:
            self.logger.error(f"Error getting page source: {str(e)}")
            raise

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def get_files_in_directory(self, directory_path: Path) -> list:
        """
        Get all files in a directory.

        Args:
            directory_path: Path to the directory

        Returns:
            list: List of file paths in the directory
        """
        return [item for item in directory_path.iterdir() if item.is_file()]

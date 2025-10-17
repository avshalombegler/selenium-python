import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from config.env_config import SHORT_TIMEOUT, LONG_TIMEOUT
from utils.logging_helper import get_logger


class BasePage:
    def __init__(self, driver, logger=None):
        self.driver = driver
        # Accept an injected logger (for tests) or use a sensible default from logging_helper
        self.logger = logger if logger is not None else get_logger(self.__class__.__name__)
        self.short_wait = SHORT_TIMEOUT
        self.long_wait = LONG_TIMEOUT

    def _safe_wait(self, ec_method, locator, timeout=None):
        """Generic wait with exception handling, no screenshot (handled by pytest hook)"""
        timeout = timeout or self.short_wait
        wait = WebDriverWait(self.driver, timeout)
        try:
            self.logger.debug(f"Waiting for {ec_method.__name__} on locator {locator} with timeout {timeout}s")
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

    @allure.step("Waiting for page to load with indicator: {indicator_locator}.")
    def wait_for_page_to_load(self, indicator_locator, timeout=None):
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
            self.logger.info(f"Waiting for page to load with indicator {indicator_locator} for {timeout}s.")
            wait.until(
                EC.visibility_of_element_located(indicator_locator),
                message=f"Page load failed: indicator {indicator_locator} not visible after {timeout}s",
            )
            self.logger.info(f"Page loaded successfully with indicator {indicator_locator}.")
        except TimeoutException as e:
            self.logger.error(f"Page load timed out after {timeout}s for indicator {indicator_locator}: {str(e)}")
            raise  # Let hook handle screenshot
        except NoSuchElementException as e:
            self.logger.error(f"Invalid locator {indicator_locator}: {str(e)}")
            raise

    def wait_for_visibility(self, locator, timeout=None):
        """Wait for element visible"""
        return self._safe_wait(EC.visibility_of_element_located, locator, timeout)

    @allure.step("Navigating to URL: {url}.")
    def navigate_to(self, url):
        self.logger.info(f"Navigating to URL: {url}.")
        self.driver.get(url)
        self.logger.info("Navigation completed.")

    def click_element(self, locator, retry_count=2):
        """Click with retry for stale/intercepted, no screenshot"""
        for attempt in range(retry_count):
            try:
                elem = self.wait_for_visibility(locator)
                self._safe_wait(EC.element_to_be_clickable, locator)
                elem.click()
                self.logger.debug(f"Clicked on {locator}")
                return
            except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                self.logger.warning(f"Click attempt {attempt+1}/{retry_count} failed for {locator}: {str(e)}")
                if attempt == retry_count - 1:
                    raise  # Let pytest hook handle screenshot

    @allure.step("Get text of element {locator}")
    def get_dynamic_element_text(self, locator, timeout=None, retry_count=2):
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
        for attempt in range(retry_count):
            try:
                self.logger.debug(f"Attempt {attempt+1}/{retry_count}: Waiting for {locator} visibility")
                elem = self.wait_for_visibility(locator, timeout)
                text = elem.text
                self.logger.debug(f"Retrieved text: {text}")
                return text
            except StaleElementReferenceException as e:
                self.logger.warning(
                    f"Attempt {attempt+1}/{retry_count}: Stale element for {locator}, retrying: {str(e)}"
                )
                if attempt == retry_count - 1:
                    self.logger.error(f"Failed to get text for {locator} after {retry_count} attempts")
                    raise
            except NoSuchElementException as e:
                self.logger.error(f"No element found for {locator}: {str(e)}")
                raise

    def get_number_of_elements(self, locator):
        self.logger.info(f"Counting elements with locator: {locator}")
        try:
            elements = WebDriverWait(self.driver, self.short_wait).until(
                EC.presence_of_all_elements_located(locator),
                message=f"Timeout waiting for elements with locator {locator}",
            )
            count = len(elements)
            self.logger.debug(f"Found {count} elements with locator {locator}")
            return count
        except TimeoutException:
            self.logger.debug(f"No elements found with locator {locator} after {SHORT_TIMEOUT}s, returning 0")
            return 0

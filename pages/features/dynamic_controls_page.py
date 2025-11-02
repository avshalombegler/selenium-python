import allure
from pages.base.base_page import BasePage
from utils.locators import DynamicControlsPageLocators
from selenium.common.exceptions import TimeoutException


class DynamicControlsPage(BasePage):
    """Page object for the Dynamic Content page containing methods to interact with and validate page functionality"""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(DynamicControlsPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click remove button")
    def click_remove_button(self):
        self.logger.info("Click remove button.")
        self.click_element(DynamicControlsPageLocators.REMOVE_BTN)
        if not self.wait_for_loader():
            self.logger.warning("Loader did not complete normally, continuing test...")

    @allure.step("Click add button")
    def click_add_button(self):
        self.logger.info("Click add button.")
        self.click_element(DynamicControlsPageLocators.ADD_BTN)
        if not self.wait_for_loader():
            self.logger.warning("Loader did not complete normally, continuing test...")

    @allure.step("Check if checkbox is present or absent")
    def is_checkbox_present(self, timeout: int = 10) -> bool:
        self.logger.info("Check if checkbox is present or absent.")
        try:
            self.wait_for_visibility(DynamicControlsPageLocators.A_CHECKBOX, timeout=timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Click enable button")
    def click_enable_button(self):
        self.logger.info("Click enable button.")
        self.click_element(DynamicControlsPageLocators.ENABLE_BTN)
        if not self.wait_for_loader():
            self.logger.warning("Loader did not complete normally, continuing test...")

    @allure.step("Click disable button")
    def click_disable_button(self):
        self.logger.info("Click disable button.")
        self.click_element(DynamicControlsPageLocators.DISABLE_BTN)
        if not self.wait_for_loader():
            self.logger.warning("Loader did not complete normally, continuing test...")

    @allure.step("Check if textbox is enabled or disabled")
    def is_textbox_enabled(self, timeout: int = 10) -> bool:
        self.logger.info("Check if textbox is enabled or disabled.")
        return self.is_element_enabled(DynamicControlsPageLocators.TEXTBOX, timeout=timeout)

    @allure.step("Get Remove/add message text")
    def get_remove_add_message(self) -> str:
        self.logger.info("Get Remove/add message text.")
        element = self.wait_for_visibility(DynamicControlsPageLocators.REMOVE_ADD_MSG)
        return element.text

    @allure.step("Get Enable/disable message text")
    def get_enable_disable_message(self) -> str:
        self.logger.info("Get Enable/disable message text.")
        element = self.wait_for_visibility(DynamicControlsPageLocators.ENABLE_DISABLE_MSG)
        return element.text

    @allure.step("Wait for loader to disappear")
    def wait_for_loader(self, timeout: int = 10):
        """
        Wait for loading indicator to appear and disappear.
        Returns True if loader completed normally, False if timeout occurred.
        """
        self.logger.info("Waiting for loader to disappear.")
        try:
            # Split timeout between appearing and disappearing
            half_timeout = max(timeout / 2, 1)  # At least 1 second each
            self.wait_for_visibility(DynamicControlsPageLocators.WAIT_LOADER, timeout=half_timeout)
            self.wait_for_invisibility(DynamicControlsPageLocators.WAIT_LOADER, timeout=half_timeout)
            return True
        except TimeoutException as e:
            self.logger.warning(f"Loader timeout after {timeout}s: {str(e)}")
            return False

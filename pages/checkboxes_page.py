import allure
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.locators import CheckboxesPageLocators


class CheckboxesPage(BasePage):
    """Page object for the Checkboxes page containing methods to interact with and validate checkboxes."""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(CheckboxesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Set checkbox '{index}' to '{should_be_checked}'")
    def set_checkbox(self, index: int, should_be_checked: bool):
        self.logger.info(f"Set checkbox '{index}' to '{should_be_checked}'.")
        if self.is_checkbox_checked(index) != should_be_checked:
            self.click_checkbox(index)

    @allure.step("Check if checkbox {index} is checked")
    def is_checkbox_checked(self, index: int) -> bool:
        locator = self.get_checkbox_locator(index)
        return self.is_element_selected(locator)

    @allure.step("Click checkbox {index}")
    def click_checkbox(self, index: int):
        locator = self.get_checkbox_locator(index)
        self.click_element(locator)

    def get_checkbox_locator(self, index: int):
        """
        Returns a locator for the checkbox at the given index (0-based).
        Example: index=0 → first checkbox, index=1 → second checkbox
        """
        # Base locator for all checkboxes
        base_locator = CheckboxesPageLocators.CHECKBOXES

        # Convert to CSS selector string
        by, value = base_locator
        if by != By.CSS_SELECTOR:
            raise ValueError("Expected CSS selector for checkboxes")

        # Add :nth-of-type(index + 1) because CSS is 1-based
        dynamic_selector = f"{value}:nth-of-type({index + 1})"

        return (By.CSS_SELECTOR, dynamic_selector)

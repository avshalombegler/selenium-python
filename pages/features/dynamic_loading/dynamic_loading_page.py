import re
import allure
from pages.base.base_page import BasePage
from pages.features.dynamic_loading.locators import DynamicLoadingPageLocators


class DynamicLoadingPage(BasePage):
    """Page object for the Dynamic Loading page containing methods to interact with and validate page functionality"""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(DynamicLoadingPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Navigate to {page_name} page")
    def click_example_1_link(self, page_name="Example 1: Element on page that is hidden"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(DynamicLoadingPageLocators.EXAMPLE_1_LINK)
        from pages.features.dynamic_loading.example_1_page import Example1Page

        return Example1Page(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_example_2_link(self, page_name="Example 2: Element rendered after the fact"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(DynamicLoadingPageLocators.EXAMPLE_2_LINK)
        from pages.features.dynamic_loading.example_2_page import Example2Page

        return Example2Page(self.driver, self.logger)

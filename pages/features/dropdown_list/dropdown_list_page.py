import allure
from selenium.webdriver.support.ui import Select
from pages.base.base_page import BasePage
from pages.features.dropdown_list.locators import DropdownListPageLocators


class DropdownListPage(BasePage):
    """Page object for the Dropdown List page containing methods to interact with and validate page functionality"""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(DropdownListPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Select option '{option}' from dropdown")
    def select_dropdown_option(self, option: str):
        select_element = self.wait_for_visibility(DropdownListPageLocators.DROPDOWN)
        select = Select(select_element)
        select.select_by_visible_text(option)

    @allure.step("Verify option '{option}' selected")
    def get_is_option_selected(self, option: str) -> bool:
        try:
            select_element = self.wait_for_visibility(DropdownListPageLocators.DROPDOWN)
            select = Select(select_element)
            selected_option = select.first_selected_option
            selected_text = selected_option.text.strip()
            self.logger.debug(f"Selected option text: '{selected_text}'")
            return selected_text == option
        except Exception as e:
            self.logger.error(f"Failed to get selected option: {e}")
            return False

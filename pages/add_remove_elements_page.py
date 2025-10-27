import allure
from pages.base_page import BasePage
from utils.locators import AddRemoveElementsPageLocators


class AddRemoveElements(BasePage):
    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(AddRemoveElementsPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Clicking Add Element button")
    def click_add_element(self):
        self.logger.info("Clicking Add Element button.")
        self.click_element(AddRemoveElementsPageLocators.ADD_ELEMENT_BTN)
        return self

    @allure.step("Clicking Delete Element button")
    def click_delete(self):
        self.logger.info("Clicking Delete Element button.")
        self.click_element(AddRemoveElementsPageLocators.DELETE_BTN)
        return self

    def count_delete_buttons(self):
        return self.get_number_of_elements(AddRemoveElementsPageLocators.DELETE_BTNS)

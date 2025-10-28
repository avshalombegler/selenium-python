import allure
from pages.base_page import BasePage
from utils.locators import AbTestingPageLocators


class ABTestingPage(BasePage):
    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(AbTestingPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Verify title")
    def get_title_text(self):
        self.logger.info("Retrieving title text from AB Testing page.")
        return self.get_dynamic_element_text(AbTestingPageLocators.TITLE)

    @allure.step("Verify paragraph content")
    def get_paragraph_text(self):
        self.logger.info("Retrieving paragraph text from AB Testing page.")
        return self.get_dynamic_element_text(AbTestingPageLocators.CONTENT_PARAGRAPH)

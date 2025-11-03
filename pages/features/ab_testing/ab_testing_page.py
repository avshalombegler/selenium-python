import allure
from pages.base.base_page import BasePage
from pages.features.ab_testing.locators import AbTestingPageLocators


class ABTestingPage(BasePage):
    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(AbTestingPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get title text")
    def get_title_text(self):
        return self.get_dynamic_element_text(AbTestingPageLocators.TITLE)

    @allure.step("Get paragraph text")
    def get_paragraph_text(self):
        return self.get_dynamic_element_text(AbTestingPageLocators.CONTENT_PARAGRAPH)

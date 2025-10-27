from pages.base_page import BasePage
from utils.locators import MainPageLocators
from pages.ab_testing_page import ABTestingPage
from pages.add_remove_elements_page import AddRemoveElements
from pages.basic_auth_page import BasicAuth
from pages.broken_images_page import BrokenImages


class MainPage(BasePage):
    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        # self.wait_for_page_to_load(MainPageLocators.PAGE_LOADED_INDICATOR)

    def click_ab_testing(self):
        self.click_element(MainPageLocators.AB_TESTING_LINK)
        return ABTestingPage(self.driver, self.logger)

    def click_add_remove_elements(self):
        self.click_element(MainPageLocators.ADD_REMOVE_ELEMENTS_LINK)
        return AddRemoveElements(self.driver, self.logger)

    def get_basic_auth(self):
        return BasicAuth(self.driver, self.logger)

    def click_broken_images(self):
        self.click_element(MainPageLocators.BROKEN_IMAGES_LINK)
        return BrokenImages(self.driver, self.logger)

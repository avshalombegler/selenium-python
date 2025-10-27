from pages.main_page import MainPage
from utils.locators import MainPageLocators
from utils.logging_helper import get_logger


class PageManager:
    def __init__(self, driver, logger=None):
        self.driver = driver
        # Use the provided logger or obtain the configured root logger so
        # all pages built by PageManager share the same logger instance.
        self.logger = logger if logger is not None else get_logger(__name__)
        self.main_page = MainPage(driver, self.logger)

    def navigate_to_base_url(self, url):
        self.main_page.navigate_to(url)
        self.main_page.wait_for_page_to_load(MainPageLocators.PAGE_LOADED_INDICATOR)
        return self.main_page

    def get_main_page(self):
        return self.main_page

    def get_ab_testing_page(self):
        return self.main_page.click_ab_testing()

    def get_add_remove_elements_page(self):
        return self.main_page.click_add_remove_elements()

    def get_basic_auth_page(self):
        return self.main_page.get_basic_auth()

    def get_broken_images_page(self):
        return self.main_page.click_broken_images()

    def get_challenging_dom_page(self):
        return self.main_page.click_challenging_dom()

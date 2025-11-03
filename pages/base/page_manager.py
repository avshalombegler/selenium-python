import allure
from pages.common.main_page.main_page import MainPage
from pages.common.main_page.locators import MainPageLocators
from utils.logging_helper import get_logger


class PageManager:
    def __init__(self, driver, logger=None):
        self.driver = driver
        # Use the provided logger or obtain the configured root logger so
        # all pages built by PageManager share the same logger instance.
        self.logger = logger if logger is not None else get_logger(__name__)
        self.main_page = MainPage(driver, self.logger)

    @allure.step("Navigate to base URL: {url}")
    def navigate_to_base_url(self, url):
        self.main_page.navigate_to(url)
        self.main_page.wait_for_page_to_load(MainPageLocators.PAGE_LOADED_INDICATOR)
        return self.main_page

    def get_ab_testing_page(self):
        return self.main_page.click_ab_testing_link()

    def get_add_remove_elements_page(self):
        return self.main_page.click_add_remove_elements_link()

    def get_basic_auth_page(self):
        return self.main_page.get_basic_auth_page()

    def get_broken_images_page(self):
        return self.main_page.click_broken_images_link()

    def get_challenging_dom_page(self):
        return self.main_page.click_challenging_dom_link()

    def get_checkboxes_page(self):
        return self.main_page.click_checkboxes_link()

    def get_context_menu_page(self):
        return self.main_page.click_context_menu_link()

    def get_digest_auth_page(self, username: str, password: str):
        if not username or not password:
            raise ValueError(f"Invalid credentials: username='{username}', password='{password or ''}'")
        url = f"https://{username}:{password}@the-internet.herokuapp.com/digest_auth"
        return self.main_page.get_digest_auth_page(url)

    def get_drag_and_drop_page(self):
        return self.main_page.click_drag_and_drop_link()

    def get_dropdown_list_page(self):
        return self.main_page.click_dropdown_list_link()

    def get_dynamic_content_page(self):
        return self.main_page.click_dynamic_content_link()

    def get_dynamic_controls_page(self):
        return self.main_page.click_dynamic_controls_link()

    def get_dynamic_loading_page(self):
        return self.main_page.click_dynamic_loading_link()

import allure
from pages.common.main_page import MainPage
from utils.locators import MainPageLocators
from utils.logging_helper import get_logger


class PageManager:
    def __init__(self, driver, logger=None):
        self.driver = driver
        # Use the provided logger or obtain the configured root logger so
        # all pages built by PageManager share the same logger instance.
        self.logger = logger if logger is not None else get_logger(__name__)
        self.main_page = MainPage(driver, self.logger)

    @allure.step("Navigate to base url")
    def navigate_to_base_url(self, url):
        self.main_page.navigate_to(url)
        self.main_page.wait_for_page_to_load(MainPageLocators.PAGE_LOADED_INDICATOR)
        return self.main_page

    def get_main_page(self):
        return self.main_page

    @allure.step("Navigate to {page_name} page")
    def get_ab_testing_page(self, page_name="A/B Testing"):
        self.logger.info(f"Navigating to {page_name} page")
        return self.main_page.click_ab_testing()

    @allure.step("Navigate to {page_name} page")
    def get_add_remove_elements_page(self, page_name="Add/Remove Elements"):
        self.logger.info(f"Navigating to {page_name} page")
        return self.main_page.click_add_remove_elements()

    @allure.step("Navigate to {page_name} page")
    def get_basic_auth_page(self, page_name="Basic Auth"):
        self.logger.info(f"Navigating to {page_name} page")
        return self.main_page.get_basic_auth()

    @allure.step("Navigate to {page_name} page")
    def get_broken_images_page(self, page_name="Broken Images"):
        self.logger.info(f"Navigating to {page_name} page")
        return self.main_page.click_broken_images()

    @allure.step("Navigate to {page_name} page")
    def get_challenging_dom_page(self, page_name="Challenging DOM"):
        self.logger.info(f"Navigating to {page_name} page")
        return self.main_page.click_challenging_dom()

    @allure.step("Navigate to {page_name} page")
    def get_checkboxes_page(self, page_name="Checkboxes"):
        self.logger.info(f"Navigating to {page_name} page")
        return self.main_page.click_checkboxes()

    @allure.step("Navigate to {page_name} page")
    def get_context_menu_page(self, page_name="Context Menu"):
        self.logger.info(f"Navigating to {page_name} page")
        return self.main_page.click_context_menu()

    @allure.step("Navigate to {page_name} page")
    def get_digest_auth_page(self, username: str, password: str, page_name="Digest Authentication"):
        self.logger.info(f"Navigating to {page_name} page")
        if not username or not password:
            raise ValueError(f"Invalid credentials: username='{username}', password='{password or ''}'")
        url = f"https://{username}:{password}@the-internet.herokuapp.com/digest_auth"
        return self.main_page.get_digest_auth(url)

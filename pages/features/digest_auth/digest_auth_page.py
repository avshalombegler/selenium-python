import allure
from pages.base.base_page import BasePage
from pages.features.digest_auth.locators import DigestAuthPageLocators
from selenium.common.exceptions import (
    TimeoutException,
)


class DigestAuthPage(BasePage):
    """Page object for the Digest Authentication page containing methods to interact with and validate page context menu"""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)

    @allure.step("Check if login succeeded")
    def is_login_successful(self):
        try:
            self.get_dynamic_element_text(DigestAuthPageLocators.AUTHORIZED_INDICATOR)
            return True
        except TimeoutException:
            return False

    @allure.step("Get page source for debug")
    def get_page_source_snippet(self):
        source = self.driver.page_source
        return source[:500]

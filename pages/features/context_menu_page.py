import allure
from pages.base.base_page import BasePage
from utils.locators import ContextMenuPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoAlertPresentException,
)


class ContextMenuPage(BasePage):
    """Page object for the Context Menu page containing methods to interact with and validate page context menu"""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(ContextMenuPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Perform right-click on page title to verify context menu alert does not activate")
    def right_click_outside_hot_spot(self, actions):
        self.logger.info("Perform right-click on page title to verify context menu alert does not activate.")
        self.perform_right_click(ContextMenuPageLocators.PAGE_LOADED_INDICATOR, actions)
        self.click_element(ContextMenuPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Perform right-click on hot-spot to verify alert activation")
    def right_click_on_hot_spot(self, actions):
        self.logger.info("Perform right-click on hot-spot to verify alert activation.")
        self.perform_right_click(ContextMenuPageLocators.HOT_SPOT_BOX, actions)

    @allure.step("Get context menu alert text")
    def get_context_menu_alert_text(self, timeout=5):
        self.logger.info("Waiting for context menu alert...")
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            text = alert.text
            self.logger.debug(f"Alert text: '{text}'")
            return text
        except TimeoutException:
            self.logger.error("Alert did not appear within timeout")
            raise NoAlertPresentException("Alert not present after right-click")

    @allure.step("Close context menu alert")
    def close_context_menu_alert(self):
        self.logger.info("Close context menu alert.")
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert.accept()

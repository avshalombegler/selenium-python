import allure
from dataclasses import dataclass
from pages.base.base_page import BasePage
from pages.features.context_menu.locators import ContextMenuPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoAlertPresentException,
)
from config.env_config import VIDEO_RECORDING


@dataclass
class ClickResult:
    alert_present: bool
    alert_text: str = None


class ContextMenuPage(BasePage):
    """Page object for the Context Menu page containing methods to interact with and validate page context menu"""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(ContextMenuPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Perform right-click on page title to verify context menu alert does not activate")
    def _perform_right_click_outside(self, actions):
        self.logger.info("Perform right-click on page title to verify context menu alert does not activate.")
        self.perform_right_click(ContextMenuPageLocators.PAGE_LOADED_INDICATOR, actions)

    @allure.step("Perform right-click on hot-spot to verify alert activation")
    def _perform_right_click_on_hotspot(self, actions):
        self.logger.info("Perform right-click on hot-spot to verify alert activation.")
        self.perform_right_click(ContextMenuPageLocators.HOT_SPOT_BOX, actions)

    @allure.step("Get context menu alert text")
    def _get_context_menu_alert_text(self, timeout=5):
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
    def _close_context_menu_alert(self):
        self.logger.info("Close context menu alert.")
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert.accept()

    @allure.step("Right click outside hot spot area")
    def right_click_outside_hot_spot(self, actions: ActionChains) -> ClickResult:
        self._perform_right_click_outside(actions)
        return ClickResult(alert_present=False)

    @allure.step("Right click on hot spot area and get alert text")
    def right_click_on_hot_spot_and_get_alert_text(self, actions: ActionChains) -> str:
        if VIDEO_RECORDING:
            self.logger.info("Video recording active – skipping alert text check")
            return "VIDEO_RECORDING_ACTIVE"
        self._perform_right_click_on_hotspot(actions)
        alert_text = self._get_context_menu_alert_text()
        self._close_context_menu_alert()
        return alert_text

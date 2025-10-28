import allure
from pages.base_page import BasePage
from utils.locators import ContextMenuPageLocators


class ContextMenuPage(BasePage):
    """Page object for the Context Menu page containing methods to interact with and validate page context menu"""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(ContextMenuPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Perform right-click on page title to verify context menu alert does not activate")
    def right_click_outside_hot_spot(self, actions):
        self.logger.info("Perform right-click on page title to verify context menu alert does not activate.")
        self.perform_right_click(ContextMenuPageLocators.PAGE_LOADED_INDICATOR, actions)

    @allure.step("Perform right-click on hot-spot to verify alert activation")
    def right_click_on_hot_spot(self, actions):
        self.logger.info("Perform right-click on hot-spot to verify alert activation.")
        self.perform_right_click(ContextMenuPageLocators.HOT_SPOT_BOX, actions)

    @allure.step("Get context menu alert text")
    def get_context_menu_alert_text(self):
        self.logger.info("Get context menu alert text.")
        return self.driver.switch_to.alert.text

    @allure.step("Close context menu alert")
    def close_context_menu_alert(self):
        self.logger.info("Close context menu alert.")
        self.driver.switch_to.alert.accept()

from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BasePage
from pages.features.exit_intent.locators import ExitIntentPageLocators

if TYPE_CHECKING:
    from logging import Logger

    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.remote.webdriver import WebDriver


class ExitIntentPage(BasePage):
    """Page object for the Exit Intent page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: WebDriver, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(ExitIntentPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Move mouse by '({x_offset}, {y_offset})' from current mouse position")
    def move_mouse_to_trigger_exit_intent(self, actions: ActionChains, x_offset: int = 0, y_offset: int = -50) -> None:
        elem = self.wait_for_visibility(ExitIntentPageLocators.PAGE_BODY)
        actions.move_to_element_with_offset(elem, x_offset, y_offset).pause(0.5).perform()

    @allure.step("Trigger exit intent via JavaScript (headless fallback)")
    def trigger_exit_intent_js(self) -> None:
        self.driver.execute_script(
            """
            var event = new Event('mouseleave');
            document.dispatchEvent(event);
        """
        )

    @allure.step("Click close window")
    def click_close_modal(self) -> None:
        self.click_element(ExitIntentPageLocators.CLOSE_BTN)

    @allure.step("Check modal window display")
    def is_modal_displayed(self) -> bool:
        return self.is_element_visible(ExitIntentPageLocators.MODAL_LOADED_INDICATOR, timeout=5)

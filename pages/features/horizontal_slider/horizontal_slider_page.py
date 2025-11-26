from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.keys import Keys

from pages.base.base_page import BasePage
from pages.features.horizontal_slider.locators import HorizontalSliderPageLocators

if TYPE_CHECKING:
    from logging import Logger

    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.remote.webdriver import WebDriver


class HorizontalSliderPage(BasePage):
    """Page object for the Horizontal Slider page containing methods to interact with and validate page functionality"""

    def __init__(
        self,
        driver: WebDriver,
        logger: Logger | None = None,
    ) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(HorizontalSliderPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Set horizontal slider value using mouse")
    def set_horizontal_slider_value_using_mouse(self, actions: ActionChains, r: int) -> None:
        slider_elem = self.wait_for_visibility(HorizontalSliderPageLocators.SLIDER)

        # Ensure element is in view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", slider_elem)
        sleep(0.5)

        # Move to element first to ensure proper positioning
        actions.move_to_element(slider_elem).pause(0.3).perform()
        actions.reset_actions()

        # Perform drag with pause
        actions.click_and_hold(slider_elem).pause(0.2).move_by_offset(r, 0).pause(0.2).release().perform()

    @allure.step("Set horizontal slider value using keys")
    def set_horizontal_slider_value_using_keys(self, actions: ActionChains, r: int) -> None:
        slider_elem = self.wait_for_visibility(HorizontalSliderPageLocators.SLIDER)

        actions.click(slider_elem).perform()
        actions.reset_actions()

        for _ in range(r):
            actions.send_keys(Keys.ARROW_LEFT).perform()
            sleep(0.5)

    @allure.step("Get horizontal slider value")
    def get_horizontal_slider_value(self) -> float:
        return float(self.get_dynamic_element_text(HorizontalSliderPageLocators.SLIDER_VALUE).strip())

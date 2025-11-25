from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.keys import Keys

from pages.base.base_page import BasePage
from pages.features.inputs.locators import InputsPageLocators

if TYPE_CHECKING:
    from logging import Logger

    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.remote.webdriver import WebDriver


class InputsPage(BasePage):
    """Page object for the Inputs page containing methods to interact with and validate page functionality"""

    def __init__(
        self,
        driver: WebDriver,
        logger: Logger | None = None,
    ) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(InputsPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Enter input number")
    def enter_input_number(self, value: int) -> None:
        self.send_keys_to_element(InputsPageLocators.INPUT_NUMBER, str(value))

    @allure.step("Increase number value by '{value}' using keyboard arrow")
    def increase_number_value(self, actions: ActionChains, value: int) -> None:
        elem = self.wait_for_visibility(InputsPageLocators.INPUT_NUMBER)
        for _ in range(value):
            actions.send_keys_to_element(elem, Keys.ARROW_UP).perform()

    @allure.step("Decrease number value by '{value}' using keyboard arrow")
    def decrease_number_value(self, actions: ActionChains, value: int) -> None:
        elem = self.wait_for_visibility(InputsPageLocators.INPUT_NUMBER)
        for _ in range(value):
            actions.send_keys_to_element(elem, Keys.ARROW_DOWN).perform()

    @allure.step("Get input number value")
    def get_input_number_value(self) -> int:
        elem = self.wait_for_visibility(InputsPageLocators.INPUT_NUMBER)
        value = self.get_element_attr_js(elem, "value")
        assert value is not None, "Input value attribute is None"
        return int(value)

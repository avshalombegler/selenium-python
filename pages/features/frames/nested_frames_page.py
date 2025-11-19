from __future__ import annotations
from typing import TYPE_CHECKING
import allure
from pages.base.base_page import BasePage
from pages.features.frames.locators import NestedFramesPageLocators

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from logging import Logger


class NestedFramesPage(BasePage):
    """Page object for the Nested Frames page containing methods to interact with and validate page functionality"""

    def __init__(
        self,
        driver: WebDriver,
        logger: Logger | None = None,
    ) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(NestedFramesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Switch to frame '{value}'")
    def switch_frame(self, value: str) -> None:
        frame_locator = (
            NestedFramesPageLocators.NESTED_FRAME[0],
            NestedFramesPageLocators.NESTED_FRAME[1].format(value=value),
        )
        self.switch_to_frame(frame_locator)

    @allure.step("Get frame text")
    def get_frame_text(self) -> str:
        return self.get_dynamic_element_text(NestedFramesPageLocators.NESTED_FRAME_BODY)

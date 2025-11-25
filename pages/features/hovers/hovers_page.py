from __future__ import annotations
from typing import TYPE_CHECKING
import allure
from pages.base.base_page import BasePage
from pages.features.hovers.locators import HoversPageLocators
from pages.features.hovers.hovers_user_page import HoversUserPage


if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from logging import Logger
    from selenium.webdriver.common.action_chains import ActionChains


class HoversPage(BasePage):
    """Page object for the Hovers page containing methods to interact with and validate page functionality"""

    def __init__(
        self,
        driver: WebDriver,
        logger: Logger | None = None,
    ) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(HoversPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Hover mouse over profile image")
    def hover_mouse_over_profile_image(self, actions: ActionChains, index: int) -> None:
        locator = (HoversPageLocators.FIGURE[0], HoversPageLocators.FIGURE[1].format(index=index))
        figure_elem = self.wait_for_visibility(locator)
        actions.move_to_element(figure_elem).perform()

    @allure.step("Get user name text")
    def get_user_name_text(self, index: int) -> str:
        locator = (HoversPageLocators.NAME[0], HoversPageLocators.NAME[1].format(index=index))
        return self.get_dynamic_element_text(locator)

    @allure.step("Click view profile link")
    def click_view_profile_link(self, index: int) -> HoversUserPage:
        locator = (HoversPageLocators.VIEW_PROFILE_BTN[0], HoversPageLocators.VIEW_PROFILE_BTN[1].format(index=index))
        self.click_element(locator)
        return HoversUserPage(self.driver, self.logger)

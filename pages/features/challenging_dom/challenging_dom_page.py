from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BasePage
from pages.features.challenging_dom.locators import ChallengingDomPageLocators

if TYPE_CHECKING:
    from logging import Logger

    from selenium.webdriver.remote.webdriver import WebDriver


class ChallengingDomPage(BasePage):
    """Page object for the Challenging DOM page containing methods to interact with and validate page web elements."""

    def __init__(self, driver: WebDriver, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(ChallengingDomPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click {button_color} button")
    def click_colored_button(self, button_color: str) -> None:
        """
        Click one of the page buttons. Case-insensitive.

        Returns self for fluent usage.
        """
        mapping = {
            "blue": ChallengingDomPageLocators.BLUE_BTN,
            "red": ChallengingDomPageLocators.RED_BTN,
            "green": ChallengingDomPageLocators.GREEN_BTN,
        }
        btn = mapping.get(button_color.lower())
        if btn is None:
            self.logger.warning(f"Unknown button color requested: {button_color}")
            return
        self.click_element(btn)

    @allure.step("Get table head text of column '{col}'")
    def get_table_head_text(self, col: str) -> None | str:
        """
        Return header text for the requested column name (exact match) or None.
        This searches the thead th elements instead of relying purely on dynamic XPATHs.
        """
        # Locate header elements directly for stability
        headers = self.get_all_elements(ChallengingDomPageLocators.TABLE_HEADERS_TEXT)
        if not headers:
            return None
        for h in headers:
            if h.text.strip() == col:
                return h.text.strip()
        # fallback to XPath approach
        xpath = ChallengingDomPageLocators.TABLE_HEAD_TEXT[1].format(column_name=col)
        return self.get_dynamic_element_text((ChallengingDomPageLocators.TABLE_HEAD_TEXT[0], xpath))

    @allure.step("Get table cell text '{cell}' under column '{col}'")
    def get_table_cell_text(self, col: str, cell: str) -> str | None:
        headers = self.get_all_elements(ChallengingDomPageLocators.TABLE_HEADERS_TEXT)
        if not headers:
            # fallback to XPath approach
            xpath = ChallengingDomPageLocators.TABLE_CELL_TEXT[1].format(column_name=col, cell_value=cell)
            return self.get_dynamic_element_text((ChallengingDomPageLocators.TABLE_CELL_TEXT[0], xpath))

        # find header index (0-based)
        try:
            idx = next(i for i, h in enumerate(headers) if h.text.strip() == col)
        except StopIteration:
            self.logger.warning(f"Column '{col}' not found in table headers.")
            return None

        # XPath that selects the td in the found column index with exact text match
        xpath = f"//div[contains(@class,'example')]//table//tbody//tr/td[{idx + 1}][normalize-space()='{cell}']"
        return self.get_dynamic_element_text((ChallengingDomPageLocators.TABLE_CELL_TEXT[0], xpath))

    @allure.step("Click edit button in row {row}")
    def click_edit_button(self, row: int) -> None:
        xpath = ChallengingDomPageLocators.EDIT_BTN[1].format(row_num=row)
        self.click_element((ChallengingDomPageLocators.EDIT_BTN[0], xpath))

    @allure.step("Click delete button in row {row}")
    def click_delete_button(self, row: int) -> None:
        xpath = ChallengingDomPageLocators.DEL_BTN[1].format(row_num=row)
        self.click_element((ChallengingDomPageLocators.DEL_BTN[0], xpath))

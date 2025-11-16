from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger


@allure.feature("Challenging DOM")
@allure.story("Verify Challenging DOM buttons interactions and table content")
@pytest.mark.usefixtures("page_manager")
class TestChallengingDom:
    """Tests for verifying Challenging DOM buttons interactions and table content"""

    EDIT_SUFFIX = "challenging_dom#edit"
    DEL_SUFFIX = "challenging_dom#delete"
    BUTTONS = ["blue", "red", "green"]
    COLUMNS = ["Lorem", "Ipsum", "Dolor", "Sit", "Amet", "Diceret"]
    CELL_VALUES = ["Iuvaret", "Apeirian", "Adipisci", "Definiebas", "Consequuntur", "Phaedrum"]

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("button", BUTTONS)
    def test_each_button_clicks(self, page_manager: PageManager, logger: Logger, button: str) -> None:
        logger.info("Verify each button in page is clickable.")
        page = page_manager.get_challenging_dom_page()

        logger.info(f"Clicking {button} button.")
        page.click_colored_button(button)

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("col", COLUMNS)
    def test_table_header_per_column(self, page_manager: PageManager, logger: Logger, col: str) -> None:
        logger.info("Verify table head text per column.")
        page = page_manager.get_challenging_dom_page()

        logger.info(f"Getting table head text of column '{col}'.")
        header = page.get_table_head_text(col)
        assert header == col, f"Table head value '{col}' not found (got '{header}')"

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("col, cell", list(zip(COLUMNS, CELL_VALUES)))
    def test_cells_content_per_column(self, page_manager: PageManager, logger: Logger, col: str, cell: str) -> None:
        logger.info("Verify cell content per column.")
        page = page_manager.get_challenging_dom_page()

        for i in range(3):  # reduced repetition for faster tests; expand as needed
            expected = f"{cell}{i}"
            logger.info(f"Getting table cell '{cell}' text under column '{col}'.")
            val = page.get_table_cell_text(col, expected)
            assert val == expected, f"Cell value '{expected}' under '{col}' not found (got '{val}')"

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_table_edit_and_delete_buttons_per_row(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Verify edit and delete buttons per row are clickable.")
        page = page_manager.get_challenging_dom_page()

        for i in range(3):  # reduced repetition for faster tests; expand as needed
            logger.info("Clicking edit button in row {i}.")
            page.click_edit_button(i)

            expected_url = page.get_base_url() + self.EDIT_SUFFIX
            curr_url = page.get_current_url()
            assert expected_url == curr_url, f"Expected URL '{expected_url}', got '{curr_url}'"

            logger.info("Click delete button in row {i}.")
            page.click_delete_button(i)

            expected_url = page.get_base_url() + self.DEL_SUFFIX
            curr_url = page.get_current_url()
            assert expected_url == curr_url, f"Expected URL '{expected_url}', got '{curr_url}'"

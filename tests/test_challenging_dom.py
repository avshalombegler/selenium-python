import pytest
import allure
from pages.page_manager import PageManager


@allure.feature("Challenging DOM")
@allure.story("Verify Challenging DOM buttons interactions and table content")
@pytest.mark.usefixtures("page_manager")
class TestChallengingDom:

    EDIT_SUFFIX = "challenging_dom#edit"
    DEL_SUFFIX = "challenging_dom#delete"
    BUTTONS = ["blue", "red", "green"]
    COLUMNS = ["Lorem", "Ipsum", "Dolor", "Sit", "Amet", "Diceret"]
    CELL_VALUES = ["Iuvaret", "Apeirian", "Adipisci", "Definiebas", "Consequuntur", "Phaedrum"]

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("button", BUTTONS)
    def test_each_button_clicks(self, page_manager: PageManager, logger, button):
        """Verify each page button can be clicked"""
        page = page_manager.get_challenging_dom_page()

        page.click_page_button(button)
        logger.info(f"Clicked {button}")

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("col, cell", list(zip(COLUMNS, CELL_VALUES)))
    def test_table_content_per_column(self, page_manager: PageManager, logger, col, cell):
        """Verify header and a sample of cell values under each column"""
        page = page_manager.get_challenging_dom_page()

        with allure.step(f"Verify header for column '{col}'"):
            header = page.get_table_head_text(col)
            assert header == col, f"Table head value '{col}' not found (got '{header}')"

        with allure.step(f"Verify cells for column '{col}' contain expected samples"):
            # check a few sample cell suffixes to ensure content is present
            for i in range(3):  # reduced repetition for faster tests; expand as needed
                expected = f"{cell}{i}"
                val = page.get_table_cell_text(col, expected)
                assert val == expected, f"Cell value '{expected}' under '{col}' not found (got '{val}')"

        with allure.step("Test edit and delete buttons"):
            for i in range(3):
                page.click_edit_button(i)

                with allure.step("Verify URL change"):
                    expected_url = page.get_base_url() + self.EDIT_SUFFIX
                    curr_url = page.get_current_url()
                    assert expected_url == curr_url, f"Expected URL '{expected_url}', got '{curr_url}'"

                page.click_delete_button(i)

                with allure.step("Verify URL change"):
                    expected_url = page.get_base_url() + self.DEL_SUFFIX
                    curr_url = page.get_current_url()
                    assert expected_url == curr_url, f"Expected URL '{expected_url}', got '{curr_url}'"

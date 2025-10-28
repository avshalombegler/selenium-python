import pytest
import allure
from pages.page_manager import PageManager


@allure.feature("Checkboxes")
@allure.story("Verify Checkboxes interactions")
@pytest.mark.usefixtures("page_manager")
class TestCheckboxes:
    @allure.severity(allure.severity_level.NORMAL)
    def test_each_button_clicks(self, page_manager: PageManager, logger):
        """Verify checkboxes functionality"""
        page = page_manager.get_checkboxes_page()

        with allure.step("Check checkboxes initial state"):
            assert not page.is_checkbox_checked(0)
            assert page.is_checkbox_checked(1)

        with allure.step("Set checkboxes new state"):
            page.set_checkbox(0, True)
            page.set_checkbox(1, False)

        with allure.step("Check checkboxes new state"):
            assert page.is_checkbox_checked(0)
            assert not page.is_checkbox_checked(1)

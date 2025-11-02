import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Checkboxes")
@allure.story("Verify Checkboxes interactions")
@pytest.mark.usefixtures("page_manager")
class TestCheckboxes:
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkboxes_functionality(self, page_manager: PageManager, logger):
        """Verify checkboxes functionality"""
        page = page_manager.get_checkboxes_page()

        logger.info("Check checkboxes initial state.")
        assert not page._is_checkbox_checked(0)
        assert page._is_checkbox_checked(1)

        logger.info("Set checkboxes new state.")
        page.set_checkbox(0, True)
        page.set_checkbox(1, False)

        logger.info("Check checkboxes new state.")
        assert page._is_checkbox_checked(0)
        assert not page._is_checkbox_checked(1)

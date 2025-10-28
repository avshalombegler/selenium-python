import pytest
import allure
from pages.page_manager import PageManager


@allure.feature("Add/Remove Elements")
@allure.story("Verify adding and removing elements on the page")
@pytest.mark.usefixtures("page_manager")
class TestAddRemoveElements:
    """Tests for add/remove elements page functionality"""

    @allure.severity(allure.severity_level.NORMAL)
    def test_add_remove_elements(self, page_manager: PageManager, logger):
        """Verify adding two elements and removing them, checking counts"""
        page = page_manager.get_add_remove_elements_page()

        with allure.step("Add two elements"):
            for _ in range(2):
                page.click_add_element()

        with allure.step("Verify 2 delete buttons exist"):
            count = page.count_delete_buttons()
            logger.info(f"Found {count} delete buttons.")
            assert count == 2, f"Expected 2 delete buttons, got {count}"

        with allure.step("Remove all elements"):
            for _ in range(2):
                page.click_delete()

        with allure.step("Verify no delete buttons remain"):
            count = page.count_delete_buttons()
            logger.info(f"Found {count} delete buttons.")
            assert count == 0, f"Expected 0 delete buttons, got {count}"

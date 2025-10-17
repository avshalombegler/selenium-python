import pytest
import allure
from pages.page_manager import PageManager


@allure.feature("Add/Remove Elements")
@allure.story("Verify adding and removing elements on the page")
@pytest.mark.usefixtures("page_manager")
class TestAddRemoveElements:
    """Tests for Add/Remove Elements page functionality"""

    @allure.severity(allure.severity_level.NORMAL)
    def test_add_remove_elements(self, page_manager: PageManager, logger):
        """Verify adding two elements and removing them, checking counts."""
        logger.info("Starting Add/Remove Elements test.")
        add_remove_page = page_manager.get_add_remove_elements_page()

        @allure.step("Add two elements.")
        def add_elements():
            for _ in range(2):
                add_remove_page.click_add_element()

        @allure.step("Verify 2 delete buttons exist.")
        def verify_two_elements():
            count = add_remove_page.count_delete_buttons()
            logger.info(f"Found {count} delete buttons.")
            assert count == 2, f"Expected 2 delete buttons, got {count}"

        @allure.step("Remove all elements.")
        def remove_elements():
            for _ in range(2):
                add_remove_page.click_delete()

        @allure.step("Verify no delete buttons remain.")
        def verify_no_elements():
            count = add_remove_page.count_delete_buttons()
            logger.info(f"Found {count} delete buttons")
            assert count == 0, f"Expected 0 delete buttons, got {count}"

        # Execute test steps
        add_elements()
        verify_two_elements()
        remove_elements()
        verify_no_elements()
        logger.info("Add/Remove Elements test completed successfully.")

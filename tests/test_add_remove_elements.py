import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Add/Remove Elements")
@allure.story("Verify adding and removing elements on the page")
@pytest.mark.usefixtures("page_manager")
class TestAddRemoveElements:
    """Tests for add/remove elements page functionality"""

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_elements(self, page_manager: PageManager, logger):
        logger.info("Tests for add elements.")
        page = page_manager.get_add_remove_elements_page()

        logger.info("Add two elements.")
        page.add_elements(2)
        count = page.count_delete_buttons()
        logger.info(f"Found {count} delete buttons.")
        assert count == 2, f"Expected 2 delete buttons, got {count}"

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_remove_elements(self, page_manager: PageManager, logger):
        logger.info("Tests for remove elements.")
        page = page_manager.get_add_remove_elements_page()

        logger.info("Ensure there are elements to remove")
        page.add_elements(2)

        logger.info("Remove all elements")
        page.remove_all_elements()
        count = page.count_delete_buttons()
        logger.info(f"Found {count} delete buttons.")
        assert count == 0, f"Expected 0 delete buttons, got {count}"

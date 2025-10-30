import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Dropdown List")
@allure.story("Tests Dropdown List functionality")
@pytest.mark.usefixtures("page_manager")
class TestDragAndDrop:
    """Tests Dropdown List functionality"""

    OPT_1 = "Option 1"
    OPT_2 = "Option 2"

    @allure.severity(allure.severity_level.NORMAL)
    def test_drag_and_drop_functionality(self, page_manager: PageManager, logger):
        page = page_manager.get_dropdown_list_page()

        logger.info(f"Select {self.OPT_1} and verify selection.")
        page.select_dropdown_option(self.OPT_1)
        assert page.get_is_option_selected(self.OPT_1), f"Expected '{self.OPT_1}' to be selected, but it's not"

        logger.info(f"Select {self.OPT_2} and verify selection.")
        page.select_dropdown_option(self.OPT_2)
        assert page.get_is_option_selected(self.OPT_2), f"Expected '{self.OPT_2}' to be selected, but it's not"

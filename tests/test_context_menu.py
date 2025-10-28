import pytest
import allure
from pages.page_manager import PageManager


@allure.feature("Context Menu")
@allure.story("Verify Context Menu interactions")
@pytest.mark.usefixtures("page_manager")
class TestCheckboxes:
    EXPECTED_ALERT_TEXT = "You selected a context menu"

    @allure.severity(allure.severity_level.NORMAL)
    def test_each_button_clicks(self, page_manager: PageManager, logger, actions):
        """Verify Context Menu interactions"""
        page = page_manager.get_context_menu_page()

        page.right_click_outside_hot_spot(actions)

        page.right_click_on_hot_spot(actions)

        with allure.step("Verify context menu alert"):
            alert_text = page.get_context_menu_alert_text()
            assert self.EXPECTED_ALERT_TEXT == alert_text

        page.close_context_menu_alert()

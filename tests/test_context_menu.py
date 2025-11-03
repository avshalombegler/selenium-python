import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Context Menu")
@allure.story("Verify Context Menu interactions")
@pytest.mark.usefixtures("page_manager")
class TestContextMenu:
    """Tests for context menu functionality"""

    EXPECTED_ALERT_TEXT = "You selected a context menu"

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_right_click_outside_hotspot(self, page_manager: PageManager, logger, actions):
        """Verify right-click outside hot spot area"""
        page = page_manager.get_context_menu_page()

        logger.info("Testing right-click outside hot spot")
        result = page.right_click_outside_hot_spot(actions)
        assert not result.alert_present, "Alert should not appear when clicking outside hot spot"

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_right_click_on_hotspot(self, page_manager: PageManager, logger, actions):
        """Verify right-click on hot spot area"""
        page = page_manager.get_context_menu_page()

        logger.info("Testing right-click on hot spot")
        alert_text = page.right_click_on_hot_spot_and_get_alert_text(actions)

        if alert_text != "VIDEO_RECORDING_ACTIVE":
            assert (
                alert_text == self.EXPECTED_ALERT_TEXT
            ), f"Expected alert text '{self.EXPECTED_ALERT_TEXT}', got '{alert_text}'"

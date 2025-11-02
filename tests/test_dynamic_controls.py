import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Dynamic Controls")
@allure.story("Tests Dynamic Controls functionality")
@pytest.mark.usefixtures("page_manager")
class TestDynamicControls:
    """Tests Dynamic Controls functionality"""

    @pytest.mark.flaky(reruns=2)
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkbox_remove_and_add(self, page_manager: PageManager, logger):
        page = page_manager.get_dynamic_controls_page()

        logger.info("Test Remove/add checkbox area.")
        assert page.is_checkbox_present()

        page.click_remove_button()
        assert not page.is_checkbox_present()
        assert "It's gone!" in page.get_remove_add_message()

        page.click_add_button()
        assert page.is_checkbox_present()
        assert "It's back!" in page.get_remove_add_message()

    @pytest.mark.flaky(reruns=2)
    @allure.severity(allure.severity_level.NORMAL)
    def test_textbox_enable_and_disable(self, page_manager: PageManager, logger):
        page = page_manager.get_dynamic_controls_page()

        logger.info("Test Enable/disable textbox area.")
        assert not page.is_textbox_enabled()

        page.click_enable_button()
        assert page.is_textbox_enabled()
        assert "It's enabled!" in page.get_enable_disable_message()

        page.click_disable_button()
        assert not page.is_textbox_enabled()
        assert "It's disabled!" in page.get_enable_disable_message()

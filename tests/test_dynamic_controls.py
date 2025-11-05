from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger


@allure.feature("Dynamic Controls")
@allure.story("Tests Dynamic Controls functionality")
@pytest.mark.usefixtures("page_manager")
class TestDynamicControls:
    """Tests Dynamic Controls functionality"""

    @pytest.mark.ui
    @pytest.mark.flaky(reruns=2)
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkbox_remove_and_add(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Test Remove/add checkbox area.")
        page = page_manager.get_dynamic_controls_page()

        logger.info("Checking if checkbox is present.")
        assert page.is_checkbox_present()

        logger.info("Clicking remove button.")
        page.click_remove_button()

        logger.info("Checking if checkbox absent.")
        assert not page.is_checkbox_present()

        logger.info("Verifying remove message text.")
        assert "It's gone!" in page.get_remove_add_message()

        logger.info("Clicking add button.")
        page.click_add_button()

        logger.info("Checking if checkbox is present.")
        assert page.is_checkbox_present()

        logger.info("Verifying add message text.")
        assert "It's back!" in page.get_remove_add_message()

    @pytest.mark.ui
    @pytest.mark.flaky(reruns=2)
    @allure.severity(allure.severity_level.NORMAL)
    def test_textbox_enable_and_disable(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Test Enable/disable textbox area.")
        page = page_manager.get_dynamic_controls_page()

        logger.info("Checking if textbox is disabled.")
        assert not page.is_textbox_enabled()

        logger.info("Clicking enable button.")
        page.click_enable_button()

        logger.info("Checking if textbox is enabled.")
        assert page.is_textbox_enabled()

        logger.info("Get enable message text.")
        assert "It's enabled!" in page.get_enable_disable_message()

        logger.info("Clicking disable button.")
        page.click_disable_button()

        logger.info("Checking if textbox is disabled.")
        assert not page.is_textbox_enabled()

        logger.info("Get disable message text.")
        assert "It's disabled!" in page.get_enable_disable_message()

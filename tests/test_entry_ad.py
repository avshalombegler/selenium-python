from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger


@allure.feature("Entry Ad")
@allure.story("Tests Entry Ad functionality")
@pytest.mark.usefixtures("page_manager")
class TestEntryAd:
    """Tests Entry Ad functionality"""

    @pytest.mark.skip(reason="Test is not yet complete")
    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_window_functionality(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Tests Entry Ad.")
        page = page_manager.get_entry_ad_page()

        logger.info("Verifying ad window display.")
        assert page.is_modal_displayed()

        logger.info("Clicking close button.")
        page.click_close_modal()

        logger.info("Verifying ad window close.")
        assert not page.is_modal_displayed()

        page.refresh_page()
        logger.info("Verifying ad window close.")
        assert not page.is_modal_displayed()

        logger.info("Clicking re-enable button.")
        page.click_re_enable_link()

        logger.info("Verifying ad window display.")
        assert page.is_modal_displayed()

        logger.info("Clicking close button.")
        page.click_close_modal()

        logger.info("Verifying ad window close.")
        assert not page.is_modal_displayed()

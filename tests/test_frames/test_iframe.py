from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger


@allure.feature("iframe")
@allure.story("Tests iframe functionality")
@pytest.mark.usefixtures("page_manager")
class TestIframe:
    """Tests iframe functionality"""

    TEXT = "Testing switch to iframe functionality"

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_iframe_functionality(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Tests iframe.")
        page = page_manager.get_frames_page()

        logger.info("Clicking iframe link.")
        iframe_page = page.click_iframe_link()

        if "read-only" in iframe_page.get_page_source(lowercase=True):
            pytest.skip("herokuapp blocked – TinyMCE read-only mode")

        logger.info("Switching to iframe.")
        iframe_page.switch_to_iframe()

        logger.info("Sending text to iframe's rich text area.")
        iframe_page.send_text_to_rich_text_area(self.TEXT)

        # TODO: Test rich text area buttons

        logger.info("Verifying text in iframe's rich text area.")
        assert self.TEXT == iframe_page.get_iframe_text()

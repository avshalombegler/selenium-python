from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger


@allure.feature("A/B Testing")
@allure.story("Verify content on A/B Testing page")
@pytest.mark.usefixtures("page_manager")
class TestABTesting:
    """Tests for verifying title and paragraph content of page"""

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_ab_testing_content(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Tests for verifying title and paragraph content of page")
        page = page_manager.get_ab_testing_page()

        title = page.get_title_text()
        logger.info(f"Retrieved title: {title}.")
        expected_titles = ["A/B Test Control", "A/B Test Variation 1"]
        assert title in expected_titles, f"Expected title in {expected_titles}, got '{title}'"

        paragraph = page.get_paragraph_text()
        logger.info(f"Retrieved paragraph: {paragraph}.")
        expected_text = "Also known as split testing"
        assert expected_text in paragraph, f"Expected '{expected_text}' in paragraph, got '{paragraph}'"

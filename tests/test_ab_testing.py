import pytest
import allure
from pages.page_manager import PageManager


@allure.feature("A/B Testing")
@allure.story("Verify content on A/B Testing page")
@pytest.mark.usefixtures("page_manager")
class TestABTesting:
    """Tests for Verifying title and paragraph content on A/B Testing page"""

    @allure.severity(allure.severity_level.NORMAL)
    def test_ab_testing_content(self, page_manager: PageManager, logger):
        with allure.step("Navigate to A/B Testing page"):
            page = page_manager.get_ab_testing_page()

        with allure.step("Verify title"):
            title = page.get_title_text()
            logger.info(f"Retrieved title: {title}.")
            expected_titles = ["A/B Test Control", "A/B Test Variation 1"]
            assert title in expected_titles, f"Expected title in {expected_titles}, got '{title}'"

        with allure.step("Verify paragraph content"):
            paragraph = page.get_paragraph_text()
            logger.info(f"Retrieved paragraph: {paragraph}.")
            expected_text = "Also known as split testing"
            assert expected_text in paragraph, f"Expected '{expected_text}' in paragraph, got '{paragraph}'"

import pytest
import allure
from pages.page_manager import PageManager


@allure.feature("A/B Testing")
@allure.story("Verify content on A/B Testing page")
@pytest.mark.usefixtures("page_manager")
class TestABTesting:
    """Tests for content on A/B Testing page"""

    @allure.severity(allure.severity_level.NORMAL)
    def test_ab_testing_content(self, page_manager: PageManager, logger):
        """Verify title and paragraph content on A/B Testing page."""
        logger.info("Starting A/B Testing test.")
        ab_page = page_manager.get_ab_testing_page()

        @allure.step("Verify title")
        def verify_title():
            title = ab_page.get_title_text()
            logger.info(f"Retrieved title: {title}.")
            expected_titles = ["A/B Test Control", "A/B Test Variation 1"]
            assert title in expected_titles, f"Expected title in {expected_titles}, got '{title}'"

        @allure.step("Verify paragraph content")
        def verify_paragraph():
            paragraph = ab_page.get_paragraph_text()
            logger.info(f"Retrieved paragraph: {paragraph}.")
            expected_text = "Also known as split testing"
            assert expected_text in paragraph, f"Expected '{expected_text}' in paragraph, got '{paragraph}'"

        # Execute test steps
        verify_title()
        verify_paragraph()
        logger.info("A/B Testing test completed successfully.")

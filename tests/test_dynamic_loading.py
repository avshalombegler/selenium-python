import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Dynamic Loading")
@allure.story("Tests Dynamic Loading functionality")
@pytest.mark.usefixtures("page_manager")
class TestDynamicLoading:
    """Tests Dynamic Loading functionality"""

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_example_1(self, page_manager: PageManager, logger):
        logger.info("Tests Dynamic Loading - Example 1.")
        page = page_manager.get_dynamic_loading_page().click_example_1_link()

        logger.info("Clicking start button.")
        page.click_start_button()

        logger.info("Verifying success message.")
        assert "Hello World!" in page.get_success_message()

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_example_2(self, page_manager: PageManager, logger):
        logger.info("Tests Dynamic Loading - Example 2.")
        page = page_manager.get_dynamic_loading_page().click_example_2_link()

        logger.info("Clicking start button.")
        page.click_start_button()

        logger.info("Verifying success message.")
        assert "Hello World!" in page.get_success_message()

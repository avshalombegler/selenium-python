import pytest
import allure
from pages.page_manager import PageManager


@allure.feature("Basic Auth")
@allure.story("")
@pytest.mark.usefixtures("page_manager")
class TestBasicAuth:
    """Tests Basic Auth login scenatios"""

    @pytest.mark.parametrize(
        "username, password, expected_message",
        [
            ("admin", "admin", "Congratulations! You must have the proper credentials."),
            ("wrong", "wrong", "Not authorized\n"),
            ("", "", "Not authorized\n"),
        ],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_basic_auth(self, page_manager: PageManager, logger, username, password, expected_message):
        logger.info("Starting Basic Auth test.")
        basic_auth_page = page_manager.get_basic_auth_page()
        url = basic_auth_page.init_url(username, password)
        basic_auth_page.navigate_using_url(url)
        message = basic_auth_page.get_auth_message()
        assert message == expected_message
        logger.info("Basic Auth test completed successfully.")

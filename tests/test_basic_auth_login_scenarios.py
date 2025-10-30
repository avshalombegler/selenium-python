import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Basic Auth")
@allure.story("Tests Basic Autorization login scenatios")
@pytest.mark.usefixtures("page_manager")
class TestBasicAuth:
    """Tests basic autorization login scenatios"""

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
        page = page_manager.get_basic_auth_page()

        url = page.init_url(username, password)
        page.navigate_using_url(url)

        message = page.get_auth_message()
        assert message == expected_message, f"Expected '{expected_message}', but got '{message}'"

from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger


@allure.feature("Basic Auth")
@allure.story("Tests Basic Autorization login scenatios")
@pytest.mark.usefixtures("page_manager")
class TestBasicAuth:
    """Tests basic autorization login scenatios"""

    @pytest.mark.parametrize(
        "username, password, expected_status_code, expected_message",
        [
            ("admin", "admin", 200, "Congratulations! You must have the proper credentials."),
            ("wrong", "wrong", 401, "Not authorized\n"),
            ("", "", 401, "Not authorized\n"),
        ],
    )
    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_basic_auth(
        self,
        page_manager: PageManager,
        logger: Logger,
        username: str,
        password: str,
        expected_status_code: int,
        expected_message: str,
    ) -> None:
        logger.info("Tests basic autorization login scenatios.")
        page = page_manager.get_basic_auth_page()

        logger.info("Initialize URL based on username and password.")
        url = page.init_url(username, password)

        logger.info("Get status code and authorization message.")
        status_code, message = page.get_status_code_and_auth_message(url)

        logger.info("Validate status code and authorization message.")
        assert expected_status_code == status_code
        assert expected_message in message

from __future__ import annotations

from typing import TYPE_CHECKING

import allure
import pytest

if TYPE_CHECKING:
    from logging import Logger

    from pages.base.page_manager import PageManager


@allure.feature("Form Authentication")
@allure.story("Tests Form Authentication functionality")
@pytest.mark.usefixtures("page_manager")
class TestFormAuthentication:
    """Tests Form Authentication functionality"""

    SUCCESSFULL_LOGIN = "You logged into a secure area!"
    SUCCESSFULL_LOGOUT = "You logged out of the secure area!"

    @pytest.mark.parametrize(
        "username, password, expected_message",
        [
            ("tomsmith", "SuperSecretPassword!", "You logged into a secure area!"),
            ("tomsmith", "wrong!", "Your password is invalid!"),
            ("wrong", "SuperSecretPassword!", "Your username is invalid!"),
        ],
    )
    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_form_authentication_functionality(
        self,
        page_manager: PageManager,
        logger: Logger,
        username: str,
        password: str,
        expected_message: str,
    ) -> None:
        logger.info("Tests Form Authentication.")
        page = page_manager.get_form_authentication_page()

        logger.info(f"Entering username '{username}'.")
        page.enter_username(username)

        logger.info(f"Entering password '{password}'.")
        page.enter_password(password)

        if self.SUCCESSFULL_LOGIN in expected_message:
            logger.info("Clicking login button.")
            secure_area_page = page.click_login_correct()

            logger.info("Verifying flash message after successfull login.")
            assert expected_message in secure_area_page.get_flash_message()

            logger.info("Clicking logout button.")
            page = secure_area_page.click_logout()

            logger.info("Verifying flash message after successfull logout.")
            assert self.SUCCESSFULL_LOGOUT in page.get_flash_message()

        else:
            logger.info("Clicking login button.")
            page.click_login_invalid()

            logger.info("Verifying flash message after unsuccessfull login.")
            assert expected_message in page.get_flash_message()

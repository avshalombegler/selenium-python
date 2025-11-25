from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger
    from selenium.webdriver.common.action_chains import ActionChains


@allure.feature("Hovers")
@allure.story("Tests Hovers functionality")
@pytest.mark.usefixtures("page_manager")
class TestHovers:
    """Tests Hovers functionality"""

    USER: str = "user"
    USERS: str = "users/"
    FIRST_USER: int = 1
    NUM_OF_USERS: int = 3

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_hovers_functionality(self, page_manager: PageManager, logger: Logger, actions: ActionChains) -> None:
        logger.info("Tests Hovers.")
        page = page_manager.get_hovers_page()

        for user_index in range(self.FIRST_USER, self.NUM_OF_USERS + 1):
            logger.info("Hovering mouse over profile image.")
            page.hover_mouse_over_profile_image(actions, user_index)

            logger.info("Getting user name text.")
            username_text = page.get_user_name_text(user_index)

            logger.info("Verifying user name text.")
            assert (
                self.USER + str(user_index) in username_text
            ), f"Expected '{username_text}' to contain '{self.USER + str(user_index)}'"

            logger.info("Clicking view profile link.")
            user_page = page.click_view_profile_link(user_index)

            logger.info("Getting current browser url.")
            current_url = user_page.get_current_browser_url()

            logger.info("Verifying user name in current url.")
            assert (
                self.USERS + str(user_index) in current_url
            ), f"Expected '{current_url}' to contain '{self.USERS + str(user_index)}'"

            logger.info("Navigating back page.")
            user_page.navigate_back_page()

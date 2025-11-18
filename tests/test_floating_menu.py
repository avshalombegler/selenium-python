from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger


@allure.feature("Floating Menu")
@allure.story("Tests Floating Menu functionality")
@pytest.mark.usefixtures("page_manager")
class TestFloatingMenu:
    """Tests Floating Menu functionality"""

    FLOATING_MENU_ITEM = [
        "Home",
        "News",
        "Contact",
        "About",
    ]

    @pytest.mark.full
    @pytest.mark.ui
    @pytest.mark.parametrize("item", FLOATING_MENU_ITEM)
    @allure.severity(allure.severity_level.NORMAL)
    def test_floating_menu_functionality(self, page_manager: PageManager, logger: Logger, item: str) -> None:
        logger.info("Tests Files Download.")
        page = page_manager.get_floating_menu_page()

        logger.info("Scroll down.")
        page.scroll_down()

        logger.info(f"Clicking floating menu item '{item}'.")
        page.click_floating_menu_item(item)

        logger.info("Verifying url updated after click on menu item.")
        assert item.lower() in page.get_current_url()

from __future__ import annotations

from typing import TYPE_CHECKING

import allure
import pytest

if TYPE_CHECKING:
    from logging import Logger

    from pages.base.page_manager import PageManager


@allure.feature("Dropdown List")
@allure.story("Tests Dropdown List functionality")
@pytest.mark.usefixtures("page_manager")
class TestDragAndDrop:
    """Tests Dropdown List functionality"""

    OPTIONS = ["Option 1", "Option 2"]

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("option", OPTIONS)
    def test_drag_and_drop_functionality(self, page_manager: PageManager, logger: Logger, option: str) -> None:
        logger.info("Tests Dropdown List functionality.")
        page = page_manager.get_dropdown_list_page()

        logger.info(f"Selecting option '{option}' from dropdown.")
        page.select_dropdown_option(option)

        logger.info(f"Verifying option '{option}' selected.")
        assert page.get_is_option_selected(option), f"Expected '{option}' to be selected, but it's not"

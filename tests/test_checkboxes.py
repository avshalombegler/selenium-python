from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger


@allure.feature("Checkboxes")
@allure.story("Verify Checkboxes interactions")
@pytest.mark.usefixtures("page_manager")
class TestCheckboxes:
    """Test for verifying checkbox functionality"""

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkboxes_functionality(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Test for verifying checkbox functionality.")
        page = page_manager.get_checkboxes_page()

        logger.info("Check checkboxes initial state.")
        assert not page.is_checkbox_checked(0)
        assert page.is_checkbox_checked(1)

        logger.info("Set checkboxes new state.")
        page.set_checkbox(0, True)
        page.set_checkbox(1, False)

        logger.info("Check checkboxes new state.")
        assert page.is_checkbox_checked(0)
        assert not page.is_checkbox_checked(1)

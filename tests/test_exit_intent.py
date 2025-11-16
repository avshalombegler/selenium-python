from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger
    from selenium.webdriver.common.action_chains import ActionChains


@allure.feature("Exit Intent")
@allure.story("Tests Exit Intent functionality")
@pytest.mark.usefixtures("page_manager")
class TestExitIntent:
    """Tests Exit Intent functionality"""

    @pytest.mark.fix
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_window_functionality(self, page_manager: PageManager, logger: Logger, actions: ActionChains) -> None:
        logger.info("Tests Exit Intent.")
        page = page_manager.get_exit_intent_page()

        logger.info("Moving mouse out of the viewport pane.")
        # page.move_mouse_to_trigger_exit_intent(actions)
        page.trigger_exit_intent_js()

        logger.info("Verifying modal display.")
        assert page.is_modal_displayed()

        logger.info("Clicking close button.")
        page.click_close_modal()

        logger.info("Verifying modal close.")
        assert not page.is_modal_displayed()

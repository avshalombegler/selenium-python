from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger
    from selenium.webdriver.common.action_chains import ActionChains


@allure.feature("Horizontal Slider")
@allure.story("Tests Horizontal Slider functionality")
@pytest.mark.usefixtures("page_manager")
class TestGeolocation:
    """Tests Horizontal Slider functionality"""

    EXPECTED_MIN_RANGE: float = 0.0
    EXPECTED_MAX_RANGE: float = 5.0
    EXPECTED_KEYS_RANGE: float = 0.5
    MIN_RANGE: int = -80
    MAX_RANGE: int = 80
    KEYS_RANGE: int = 4

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_horizontal_slider_functionality_using_mouse(
        self, page_manager: PageManager, logger: Logger, actions: ActionChains
    ) -> None:
        logger.info("Tests Horizontal Slider.")
        page = page_manager.get_horizontal_slider_page()

        logger.info("Setting horizontal slider value using drag and drop.")
        page.set_horizontal_slider_value_using_mouse(actions, self.MAX_RANGE)

        logger.info("Verifying horizontal slider new value.")
        assert self.EXPECTED_MAX_RANGE == page.get_horizontal_slider_value()

        logger.info("Setting horizontal slider value using drag and drop.")
        page.set_horizontal_slider_value_using_mouse(actions, self.MIN_RANGE)

        logger.info("Verifying horizontal slider new value.")
        assert self.EXPECTED_MIN_RANGE == page.get_horizontal_slider_value()

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_horizontal_slider_functionality_using_keys(
        self, page_manager: PageManager, logger: Logger, actions: ActionChains
    ) -> None:
        logger.info("Tests Horizontal Slider.")
        page = page_manager.get_horizontal_slider_page()

        logger.info("Setting horizontal slider value using arrow key.")
        page.set_horizontal_slider_value_using_keys(actions, self.KEYS_RANGE)

        logger.info("Verifying horizontal slider new value.")
        assert self.EXPECTED_KEYS_RANGE == page.get_horizontal_slider_value()

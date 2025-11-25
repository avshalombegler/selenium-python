from __future__ import annotations

from typing import TYPE_CHECKING

import allure
import pytest

if TYPE_CHECKING:
    from logging import Logger

    from selenium.webdriver.common.action_chains import ActionChains

    from pages.base.page_manager import PageManager


@allure.feature("Inputs")
@allure.story("Tests Inputs functionality")
@pytest.mark.usefixtures("page_manager")
class TestInfiniteScroll:
    """Tests Inputs functionality"""

    NUMBER: int = 1337
    INCREASE_VALUE: int = 5
    DECREASE_VALUE: int = 2
    EXPECTED_VALUE: int = NUMBER + INCREASE_VALUE - DECREASE_VALUE

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_inputs_functionality(self, page_manager: PageManager, logger: Logger, actions: ActionChains) -> None:
        logger.info("Tests Inputs.")
        page = page_manager.get_inputs_page()

        logger.info("Entering input number.")
        page.enter_input_number(self.NUMBER)

        logger.info("Getting input number value.")
        input_number = page.get_input_number_value()

        logger.info("Getting input number value.")
        assert self.NUMBER == input_number

        logger.info("Increasing number value using keyboard arrow.")
        page.increase_number_value(actions, self.INCREASE_VALUE)

        logger.info("Getting input number value.")
        increased_number = page.get_input_number_value()

        logger.info("Getting input number value.")
        assert self.NUMBER + self.INCREASE_VALUE == increased_number

        logger.info("Decreasing number value using keyboard arrow.")
        page.decrease_number_value(actions, self.DECREASE_VALUE)

        logger.info("Getting input number value.")
        decreased_number = page.get_input_number_value()

        logger.info("Getting input number value.")
        assert self.EXPECTED_VALUE == decreased_number

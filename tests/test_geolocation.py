from __future__ import annotations

from typing import TYPE_CHECKING

import allure
import pytest

if TYPE_CHECKING:
    from logging import Logger

    from pages.base.page_manager import PageManager

LAT_VAL = 32.0853
LONG_VAL = 34.7818


@allure.feature("Geolocation")
@allure.story("Tests Geolocation functionality")
@pytest.mark.usefixtures("page_manager")
class TestGeolocation:
    """Tests Geolocation functionality"""

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_geolocation_functionality(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Tests Geolocation.")
        page = page_manager.get_geolocation_page()

        logger.info("Clicking 'Where am I' button.")
        page.click_where_am_i_button()

        logger.info("Verifying geolocation latitude value.")
        lat = page.get_latitude_value()
        assert LAT_VAL == lat, f"expected '{LAT_VAL}', but got '{lat}'"

        logger.info("Verifying geolocation longitude value.")
        long = page.get_longitude_value()
        assert LONG_VAL == long, f"expected '{LONG_VAL}', but got '{long}'"

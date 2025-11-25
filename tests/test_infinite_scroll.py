from __future__ import annotations

from typing import TYPE_CHECKING

import allure
import pytest

if TYPE_CHECKING:
    from logging import Logger

    from pages.base.page_manager import PageManager


@allure.feature("Infinite Scroll")
@allure.story("Tests Infinite Scroll functionality")
@pytest.mark.usefixtures("page_manager")
class TestInfiniteScroll:
    """Tests Infinite Scroll functionality"""

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_infinite_scroll_functionality(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Tests Infinite Scroll.")
        page = page_manager.get_infinite_scroll_page()

        for _ in range(5):
            logger.info("Getting old page height.")
            old_height = page.get_page_height()

            logger.info("Scrolling to bottom of page.")
            page.scroll_to_bottom_of_page()

            logger.info("Getting new page height.")
            new_height = page.get_page_height()

            logger.info("Verifying new page height is bigger than old page height.")
            assert old_height < new_height, (
                f"Expected 'old height < new height', but got 'old height: {old_height} < height: {new_height}'"
            )

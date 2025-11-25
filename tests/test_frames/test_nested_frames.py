from __future__ import annotations

from typing import TYPE_CHECKING

import allure
import pytest

if TYPE_CHECKING:
    from logging import Logger

    from pages.base.page_manager import PageManager


@allure.feature("Nested Frames")
@allure.story("Tests Nested Frames functionality")
@pytest.mark.usefixtures("page_manager")
class TestNestedFrames:
    """Tests Nested Frames functionality"""

    TOP_FRAME = "top"
    BOTTOM_FRAME = "bottom"
    NESTED_FRAMES = ["left", "middle", "right"]

    @pytest.mark.full
    @pytest.mark.ui
    @pytest.mark.parametrize("frame", NESTED_FRAMES)
    @allure.severity(allure.severity_level.NORMAL)
    def test_top_nested_frames_functionality(self, page_manager: PageManager, logger: Logger, frame: str) -> None:
        logger.info("Tests Nested Frames.")
        page = page_manager.get_frames_page()

        logger.info("Clicking Nested Frames link.")
        nested_frames_page = page.click_nested_frames_link()

        logger.info(f"Switching to frame '{self.TOP_FRAME}'.")
        nested_frames_page.switch_frame(self.TOP_FRAME)

        logger.info(f"Switching to nested frame '{frame}'.")
        nested_frames_page.switch_frame(frame)

        logger.info("Verifying frame text.")
        assert frame.upper() == nested_frames_page.get_frame_text()

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_bottom_nested_frames_functionality(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Tests Nested Frames.")
        page = page_manager.get_frames_page()

        logger.info("Clicking Nested Frames link.")
        nested_frames_page = page.click_nested_frames_link()

        logger.info(f"Switching to frame '{self.BOTTOM_FRAME}'.")
        nested_frames_page.switch_frame(self.BOTTOM_FRAME)

        logger.info("Verifying frame text.")
        assert self.BOTTOM_FRAME.upper() == nested_frames_page.get_frame_text()

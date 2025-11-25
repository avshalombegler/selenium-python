from __future__ import annotations

from typing import TYPE_CHECKING

import allure
import pytest

if TYPE_CHECKING:
    from logging import Logger

    from pages.base.page_manager import PageManager


@allure.feature("Dynamic Content")
@allure.story("Tests Dynamic Content functionality")
@pytest.mark.usefixtures("page_manager")
class TestDynamicContent:
    """Tests for Dynamic Content functionality"""

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_content_changes_after_refresh(self, page_manager: PageManager, logger: Logger) -> None:
        logger.info("Test that content changes after page refresh.")

        page = page_manager.get_dynamic_content_page()
        initial_blocks = page.get_all_content_blocks()

        page.refresh_page()
        refreshed_blocks = page.get_all_content_blocks()

        logger.info("Validating initial content blocks structure and count.")
        self._validate_blocks_count(initial_blocks)
        self._validate_blocks_structure(initial_blocks)

        logger.info("Validating refreshed content blocks structure and count.")
        self._validate_blocks_count(refreshed_blocks)
        self._validate_blocks_structure(refreshed_blocks)

        logger.info("Comparing content changes after refresh.")
        changed_count = self._count_changed_blocks(initial_blocks, refreshed_blocks)
        assert 0 < changed_count <= 3, f"Expected 1-3 blocks to change, got {changed_count}"

    def _validate_blocks_count(self, blocks: list) -> None:
        """Validate that we have exactly 3 content blocks"""
        assert len(blocks) == 3, f"Expected 3 content blocks, got {len(blocks)}"

    def _validate_blocks_structure(self, blocks: list) -> None:
        """Validate structure of each content block"""
        for block in blocks:
            assert block["image"].startswith("http"), "Invalid image URL"
            assert block["text"].strip(), "Empty text in block"

    def _count_changed_blocks(self, initial_blocks: list, refreshed_blocks: list) -> int:
        """Count how many blocks changed between refreshes"""
        return sum(
            1
            for i in range(3)
            if (
                initial_blocks[i]["image"] != refreshed_blocks[i]["image"]
                or initial_blocks[i]["text"] != refreshed_blocks[i]["text"]
            )
        )

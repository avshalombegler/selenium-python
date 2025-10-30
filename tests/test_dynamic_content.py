import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Dynamic Content")
@allure.story("Tests Dynamic Content functionality")
@pytest.mark.usefixtures("page_manager")
class TestDynamicContent:
    """Tests Dynamic Content functionality"""

    @allure.severity(allure.severity_level.NORMAL)
    def test_dynamic_content_functionality(self, page_manager: PageManager, logger):
        page = page_manager.get_dynamic_content_page()

        initial_blocks = page.get_all_content_blocks()

        page.refresh_page()

        refreshed_blocks = page.get_all_content_blocks()

        assert len(initial_blocks) == 3, "Expected 3 content blocks"
        assert len(refreshed_blocks) == 3, "Expected 3 blocks after refresh"

        for blocks in [initial_blocks, refreshed_blocks]:
                for block in blocks:
                    assert block["image"].startswith("http"), "Invalid image URL"
                    assert block["text"].strip(), "Empty text in block"

        changed_blocks = 0
        for i in range(3):
            if (initial_blocks[i]["image"] != refreshed_blocks[i]["image"] or
                initial_blocks[i]["text"] != refreshed_blocks[i]["text"]):
                changed_blocks += 1

        assert changed_blocks > 0, "No content changed after refresh"
        assert changed_blocks <= 3, "Expected 1-3 blocks to change"
import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Drag and Drop")
@allure.story("Tests Drag and Drop functionality")
@pytest.mark.usefixtures("page_manager")
class TestDragAndDrop:
    """Tests Drag and Drop functionality"""

    BOX_A = "A"
    BOX_B = "B"

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_drag_and_drop_functionality(self, page_manager: PageManager, logger, actions):
        logger.info("Tests Drag and Drop functionality.")
        page = page_manager.get_drag_and_drop_page()

        logger.info("Getting box elements for drag and drop.")
        src = page.get_box_element(self.BOX_A.lower())
        dst = page.get_box_element(self.BOX_B.lower())

        logger.info("Performing drag and drop on box element.")
        page.drag_and_drop_box(actions, src, dst)

        logger.info("Verifying drag and drop action succeeded.")
        assert page.get_box_header(self.BOX_A.lower()) == self.BOX_B
        assert page.get_box_header(self.BOX_B.lower()) == self.BOX_A

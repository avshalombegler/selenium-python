import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Broken Images")
@allure.story("Verify the correct number of broken and valid images on the page")
@pytest.mark.usefixtures("page_manager")
class TestBrokenImages:

    EXPECTED_BROKEN_IMAGES = 2
    EXPECTED_VALID_IMAGES = 1

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_broken_images_count(self, page_manager: PageManager, logger):
        """Verify the number of broken images on the page."""
        page = page_manager.get_broken_images_page()

        broken_count = page.get_broken_images_count()
        logger.info(f"Found {broken_count} broken images")
        assert (
            broken_count == self.EXPECTED_BROKEN_IMAGES
        ), f"Expected {self.EXPECTED_BROKEN_IMAGES} broken images, found {broken_count}"

    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_valid_images_count(self, page_manager: PageManager, logger):
        """Verify the number of valid images on the page."""
        page = page_manager.get_broken_images_page()

        valid_count = page.get_valid_images_count()
        logger.info(f"Found {valid_count} valid images")
        assert (
            valid_count == self.EXPECTED_VALID_IMAGES
        ), f"Expected {self.EXPECTED_VALID_IMAGES} valid images, found {valid_count}"

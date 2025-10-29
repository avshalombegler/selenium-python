import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Broken Images")
@allure.story("Verify the correct number of broken and valid images on the page")
@pytest.mark.usefixtures("page_manager")
class TestBrokenImages:

    EXPECTED_BROKEN_IMAGES = 2
    EXPECTED_VALID_IMAGES = 1

    @allure.severity(allure.severity_level.NORMAL)
    def test_broken_images(self, page_manager: PageManager, logger):
        """Verify the correct number of broken and valid images on the page."""
        page = page_manager.get_broken_images_page()

        images = page.get_all_images()
        assert images, "No images found on the page"

        with allure.step("Analyze images"):
            results = [page.is_image_broken(img) for img in images]

        broken = [img for img in results if img["is_broken"]]
        valid = [img for img in results if not img["is_broken"]]

        with allure.step("Verify image counts"):
            assert (
                len(broken) == self.EXPECTED_BROKEN_IMAGES
            ), f"Expected {self.EXPECTED_BROKEN_IMAGES} broken images, found {len(broken)}"
            assert (
                len(valid) == self.EXPECTED_VALID_IMAGES
            ), f"Expected {self.EXPECTED_VALID_IMAGES} valid images, found {len(valid)}"

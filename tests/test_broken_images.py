import pytest
import allure
from pages.page_manager import PageManager


@allure.feature("Broken Images")
@allure.story("Verifying visibility of images")
@pytest.mark.usefixtures("page_manager")
class TestBrokenImages:
    """Tests for verifying visibility of images"""

    @allure.severity(allure.severity_level.NORMAL)
    def test_broken_images(self, page_manager: PageManager, logger):
        logger.info("Starting Broken Images test.")
        broken_images_page = page_manager.get_broken_images_page()
        images_elements = broken_images_page.get_all_images()
        broken_images = []
        valid_images = []
        for image in images_elements:
            image_results = broken_images_page.is_image_broken(image)
            if image_results["is_broken"]:
                broken_images.append(image_results)
            else:
                valid_images.append(image_results)

        # for testing if any image is broken
        # assert broken_images.len == 0

        # for testing if exact images are broken
        assert len(broken_images) is 2
        assert len(valid_images) is 1

        logger.info("Broken Images test completed successfully.")

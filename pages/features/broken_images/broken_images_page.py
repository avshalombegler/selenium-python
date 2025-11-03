import allure
from pages.base.base_page import BasePage
from pages.features.broken_images.locators import BrokenImagesPageLocators


class BrokenImagesPage(BasePage):
    """Page object for the Broken Images page containing methods to interact with and validate images."""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(BrokenImagesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get all image elements")
    def _get_all_images(self) -> list:
        self.logger.info("Get all image elements.")
        return self.get_all_elements(BrokenImagesPageLocators.IMAGES)

    @allure.step("Check if image is broken")
    def _is_image_broken(self, image) -> dict:
        """
        Check if an image is broken by verifying its natural width.

        Args:
            image: WebElement representing the image

        Returns:
            dict: Contains image source, broken status and natural width
        """
        self.logger.info("Check if image is broken.")
        src = image.get_attribute("src")
        natural_width = self.get_element_attr_js(image, "naturalWidth")

        return {"src": src, "is_broken": not natural_width, "natural_width": natural_width}

    @allure.step("Get count of broken images")
    def get_broken_images_count(self) -> int:
        images = self._get_all_images()
        results = [self._is_image_broken(img) for img in images]
        return len([img for img in results if img["is_broken"]])

    @allure.step("Get count of valid images")
    def get_valid_images_count(self) -> int:
        images = self._get_all_images()
        results = [self._is_image_broken(img) for img in images]
        return len([img for img in results if not img["is_broken"]])

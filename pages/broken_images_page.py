import allure
from pages.base_page import BasePage
from utils.locators import BrokenImagesPageLocators


class BrokenImages(BasePage):
    """Page object for the Broken Images page containing methods to interact with and validate images."""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(BrokenImagesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Getting all image elements.")
    def get_all_images(self) -> list:
        self.logger.info("Getting all image elements.")
        return self.get_all_elements(BrokenImagesPageLocators.IMAGES)

    @allure.step("Checking if image is broken")
    def is_image_broken(self, image) -> dict:
        """
        Check if an image is broken by verifying its natural width.

        Args:
            image: WebElement representing the image

        Returns:
            dict: Contains image source, broken status and natural width
        """
        self.logger.info("Checking if image is broken.")
        src = image.get_attribute("src")
        natural_width = self.get_element_attr_js(image, "naturalWidth")

        return {"src": src, "is_broken": not natural_width, "natural_width": natural_width}

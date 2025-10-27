import allure
from pages.base_page import BasePage
from utils.locators import BrokenImagesPageLocators


class BrokenImages(BasePage):
    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(BrokenImagesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Getting all image elements.")
    def get_all_images(self):
        self.logger.info("Getting all image elements.")
        images = self.get_all_elements(BrokenImagesPageLocators.IMAGES)
        return images

    # @allure.step("Checking image {image.get_attribute('src')}.")
    def is_image_broken(self, image):
        self.logger.info("Verify if image is broken.")
        natural_width = self.get_element_attr_js(image, "naturalWidth")
        if natural_width:
            return {"src": image.get_attribute("src"), "is_broken": False, "natural_width": natural_width}
        else:
            return {"src": image.get_attribute("src"), "is_broken": True, "natural_width": natural_width}

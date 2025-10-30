import allure
from pages.base.base_page import BasePage
from utils.locators import DynamicContentPageLocators


class DynamicContentPage(BasePage):
    """Page object for the Dynamic Content page containing methods to interact with and validate page functionality"""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(DynamicContentPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get all content blocks data")
    def get_all_content_blocks(self):
        blocks = self.get_all_elements(DynamicContentPageLocators.CONTENT_BLOCKS)
        data = []
        for block in blocks:
            try:
                img = block.find_element(*DynamicContentPageLocators.IMAGE_IN_BLOCK).get_attribute("src")
                text = block.find_element(*DynamicContentPageLocators.TEXT_IN_BLOCK).text.strip()
                data.append({"image": img, "text": text})
            except:
                self.logger.warning("Failed to parse block content")
                continue
        return data

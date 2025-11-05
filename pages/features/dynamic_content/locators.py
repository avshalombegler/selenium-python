"""
Module containing locators for Dynamic Content page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class DynamicContentPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    CONTENT_BLOCKS: Locator = (By.CSS_SELECTOR, "#content > .row")
    IMAGE_IN_BLOCK: Locator = (By.CSS_SELECTOR, "div#content div.large-2 img")
    TEXT_IN_BLOCK: Locator = (By.CSS_SELECTOR, "div#content div.large-2 + div.large-10")

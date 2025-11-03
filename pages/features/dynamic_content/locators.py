"""
Module containing locators for Dynamic Content page object.
"""

from selenium.webdriver.common.by import By


class DynamicContentPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    CONTENT_BLOCKS = (By.CSS_SELECTOR, "#content > .row")
    IMAGE_IN_BLOCK = (By.CSS_SELECTOR, "div#content div.large-2 img")
    TEXT_IN_BLOCK = (By.CSS_SELECTOR, "div#content div.large-2 + div.large-10")

"""
Module containing locators for Broken Images page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class BrokenImagesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    IMAGES: Locator = (By.CSS_SELECTOR, "div.example img")

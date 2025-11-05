"""
Module containing locators for Broken Images page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class BrokenImagesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    IMAGES: Locator = (By.CSS_SELECTOR, "div.example img")

"""
Module containing locators for Broken Images page object.
"""

from selenium.webdriver.common.by import By


class BrokenImagesPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    IMAGES = (By.CSS_SELECTOR, "div.example img")

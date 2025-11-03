"""
Module containing locators for Context Menu page object.
"""

from selenium.webdriver.common.by import By


class ContextMenuPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    HOT_SPOT_BOX = (By.CSS_SELECTOR, "div#hot-spot")

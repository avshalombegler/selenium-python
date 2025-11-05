"""
Module containing locators for Context Menu page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class ContextMenuPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    HOT_SPOT_BOX: Locator = (By.CSS_SELECTOR, "div#hot-spot")

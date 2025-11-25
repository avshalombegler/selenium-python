"""
Module containing locators for Context Menu page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class ContextMenuPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    HOT_SPOT_BOX: Locator = (By.CSS_SELECTOR, "div#hot-spot")

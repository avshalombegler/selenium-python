"""
Module containing locators for Floating Menu page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class FloatingMenuPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    MENU_ITEM: Locator = (By.LINK_TEXT, "{item}")

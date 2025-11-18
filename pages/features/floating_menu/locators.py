"""
Module containing locators for Files Download page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class FloatingMenuPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    MENU_ITEM: Locator = (By.LINK_TEXT, "{item}")

"""
Module containing locators for Infinite Scroll pages object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class InfiniteScrollPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")

"""
Module containing locators for Dropdown List page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class DropdownListPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    DROPDOWN: Locator = (By.CSS_SELECTOR, "select#dropdown")
    OPTION: Locator = (By.NAME, "{val}")

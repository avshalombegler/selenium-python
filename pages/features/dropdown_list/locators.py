"""
Module containing locators for Dropdown List page object.
"""

from selenium.webdriver.common.by import By


class DropdownListPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    DROPDOWN = (By.CSS_SELECTOR, "select#dropdown")
    OPTION = (By.NAME, "{val}")

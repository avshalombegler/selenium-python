"""
Module containing locators for Checkboxes page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class CheckboxesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    CHECKBOXES: Locator = (By.CSS_SELECTOR, "form#checkboxes input[type=checkbox]")

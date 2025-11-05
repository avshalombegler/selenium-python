"""
Module containing locators for Checkboxes page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class CheckboxesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    CHECKBOXES: Locator = (By.CSS_SELECTOR, "form#checkboxes input[type='checkbox']")

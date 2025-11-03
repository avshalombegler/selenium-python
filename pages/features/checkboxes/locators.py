"""
Module containing locators for Checkboxes page object.
"""

from selenium.webdriver.common.by import By


class CheckboxesPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    CHECKBOXES = (By.CSS_SELECTOR, "form#checkboxes input[type='checkbox']")

"""
Module containing locators for Dynamic Controls page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class DynamicControlsPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h4")
    WAIT_LOADER: Locator = (By.CSS_SELECTOR, "#loading")

    A_CHECKBOX: Locator = (By.CSS_SELECTOR, "input[type='checkbox']")
    REMOVE_BTN: Locator = (By.XPATH, "//button[text()='Remove']")
    ADD_BTN: Locator = (By.XPATH, "//button[text()='Add']")
    REMOVE_ADD_MSG: Locator = (By.CSS_SELECTOR, "#checkbox-example #message")

    TEXTBOX: Locator = (By.CSS_SELECTOR, "input[type='text']")
    ENABLE_BTN: Locator = (By.XPATH, "//button[text()='Enable']")
    DISABLE_BTN: Locator = (By.XPATH, "//button[text()='Disable']")
    ENABLE_DISABLE_MSG: Locator = (By.CSS_SELECTOR, "#input-example #message")

"""
Module containing locators for Dynamic Controls page object.
"""

from selenium.webdriver.common.by import By


class DynamicControlsPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, ".example h4")
    WAIT_LOADER = (By.CSS_SELECTOR, "#loading")

    A_CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    REMOVE_BTN = (By.XPATH, "//button[text()='Remove']")
    ADD_BTN = (By.XPATH, "//button[text()='Add']")
    REMOVE_ADD_MSG = (By.CSS_SELECTOR, "#checkbox-example #message")

    TEXTBOX = (By.CSS_SELECTOR, "input[type='text']")
    ENABLE_BTN = (By.XPATH, "//button[text()='Enable']")
    DISABLE_BTN = (By.XPATH, "//button[text()='Disable']")
    ENABLE_DISABLE_MSG = (By.CSS_SELECTOR, "#input-example #message")

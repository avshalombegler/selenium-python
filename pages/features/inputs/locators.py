"""
Module containing locators for Inputs pages object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class InputsPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "h3")
    INPUT_NUMBER: Locator = (By.CSS_SELECTOR, "input[type=number]")

"""
Module containing locators for Add Remove Elements page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class AddRemoveElementsPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div#content h3")
    ADD_ELEMENT_BTN: Locator = (By.CSS_SELECTOR, ".example > button")
    DELETE_BTN: Locator = (By.CSS_SELECTOR, "#elements > button:first-child")
    DELETE_BTNS: Locator = (By.CSS_SELECTOR, "#elements > button")

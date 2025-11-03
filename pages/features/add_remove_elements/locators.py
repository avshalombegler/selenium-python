"""
Module containing locators for Add Remove Elements page object.
"""

from selenium.webdriver.common.by import By


class AddRemoveElementsPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div#content h3")
    ADD_ELEMENT_BTN = (By.CSS_SELECTOR, ".example > button")
    DELETE_BTN = (By.CSS_SELECTOR, "#elements > button:first-child")
    DELETE_BTNS = (By.CSS_SELECTOR, "#elements > button")

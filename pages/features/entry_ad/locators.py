"""
Module containing locators for Entry Ad page object.
"""

from selenium.webdriver.common.by import By


class EntryAdPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, ".example h3")
    MODAL_LOADED_INDICATOR = (By.CSS_SELECTOR, ".modal-title h3")
    CLOSE_BTN = (By.CSS_SELECTOR, "div.modal-footer p")
    RE_ENABLE_LINK = (By.LINK_TEXT, "click here")

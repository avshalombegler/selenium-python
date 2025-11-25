"""
Module containing locators for Entry Ad page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class EntryAdPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    MODAL_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".modal-title h3")
    CLOSE_BTN: Locator = (By.CSS_SELECTOR, "div.modal-footer p")
    RE_ENABLE_LINK: Locator = (By.LINK_TEXT, "click here")

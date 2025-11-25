"""
Module containing locators for Exit Intent page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class ExitIntentPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    PAGE_BODY: Locator = (By.TAG_NAME, "body")
    MODAL_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".modal-title h3")
    CLOSE_BTN: Locator = (By.CSS_SELECTOR, "div.modal-footer p")

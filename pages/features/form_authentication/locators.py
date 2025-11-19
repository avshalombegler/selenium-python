"""
Module containing locators for Form Authentication page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class FormAuthenticationPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h2")
    USERNAME_TEXTBOX: Locator = (By.ID, "username")
    PASSWORD_TEXTBOX: Locator = (By.ID, "password")
    LOGIN_BTN: Locator = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MSG: Locator = (By.ID, "flash")


class SecureAreaPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h2")
    LOGOUT_BTN: Locator = (By.CSS_SELECTOR, "a[href='/logout']")
    FLASH_MSG: Locator = (By.ID, "flash")

"""
Module containing locators for Basic Auth page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class BasicAuthPageLocators:
    AUTHORIZED_INDICATOR: Locator = (By.CSS_SELECTOR, "div#content p")

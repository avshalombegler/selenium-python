"""
Module containing locators for Digest Auth page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class DigestAuthPageLocators:
    AUTHORIZED_INDICATOR: Locator = (By.CSS_SELECTOR, "div#content p")

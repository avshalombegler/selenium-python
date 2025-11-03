"""
Module containing locators for Digest Auth page object.
"""

from selenium.webdriver.common.by import By


class DigestAuthPageLocators:
    AUTHORIZED_INDICATOR = (By.CSS_SELECTOR, "div#content p")

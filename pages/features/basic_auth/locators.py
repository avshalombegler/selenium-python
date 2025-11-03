"""
Module containing locators for Basic Auth page object.
"""

from selenium.webdriver.common.by import By


class BasicAuthPageLocators:
    AUTHORIZED_INDICATOR = (By.CSS_SELECTOR, "div#content p")

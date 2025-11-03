"""
Module containing locators for AB Testing page object.
"""

from selenium.webdriver.common.by import By


class AbTestingPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    TITLE = (By.CSS_SELECTOR, "div.example h3")
    CONTENT_PARAGRAPH = (By.CSS_SELECTOR, "div#content p")

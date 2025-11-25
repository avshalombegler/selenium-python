"""
Module containing locators for AB Testing page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class AbTestingPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    TITLE: Locator = (By.CSS_SELECTOR, "div.example h3")
    CONTENT_PARAGRAPH: Locator = (By.CSS_SELECTOR, "div#content p")

"""
Module containing locators for Dynamic Loading page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class DynamicLoadingPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    EXAMPLE_1_LINK: Locator = (By.LINK_TEXT, "Example 1: Element on page that is hidden")
    EXAMPLE_2_LINK: Locator = (By.LINK_TEXT, "Example 2: Element rendered after the fact")


class Example1PageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h4")
    START_BTN: Locator = (By.CSS_SELECTOR, "div#start >button")
    WAIT_LOADER: Locator = (By.CSS_SELECTOR, "div#loading")
    SUCCESS_MSG: Locator = (By.CSS_SELECTOR, "div#finish > h4")


class Example2PageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, ".example h4")
    START_BTN = (By.CSS_SELECTOR, "div#start >button")
    WAIT_LOADER = (By.CSS_SELECTOR, "div#loading")
    SUCCESS_MSG = (By.CSS_SELECTOR, "div#finish > h4")

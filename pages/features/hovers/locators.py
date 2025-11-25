"""
Module containing locators for Hovers pages object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class HoversPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    FIGURE: Locator = (By.CSS_SELECTOR, "div.figure:nth-of-type({index})")
    NAME: Locator = (By.CSS_SELECTOR, "div.figure:nth-of-type({index}) > .figcaption > h5")
    VIEW_PROFILE_BTN: Locator = (By.CSS_SELECTOR, "div.figure:nth-of-type({index}) > .figcaption > a")


class HoversUserPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "h1")

"""
Module containing locators for Horizontal Slider pages object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class HorizontalSliderPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    SLIDER: Locator = (By.CSS_SELECTOR, "input[type='range']")
    SLIDER_VALUE: Locator = (By.ID, "range")

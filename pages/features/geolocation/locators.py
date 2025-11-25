"""
Module containing locators for Geolocation pages object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class GeolocationPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    WHERE_AM_I_BTN: Locator = (By.CSS_SELECTOR, "button[onclick='getLocation()']")
    LAT_VAL: Locator = (By.ID, "lat-value")
    LONG_VAL: Locator = (By.ID, "long-value")

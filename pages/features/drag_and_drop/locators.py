"""
Module containing locators for Drag And Drop page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class DragAndDropPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    BOX: Locator = (By.CSS_SELECTOR, "div#column-{box}")
    BOX_HEADER: Locator = (By.CSS_SELECTOR, "div#column-{box} header")

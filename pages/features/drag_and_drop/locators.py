"""
Module containing locators for Drag And Drop page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class DragAndDropPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "div.example h3")
    BOX: Locator = (By.CSS_SELECTOR, "div#column-{box}")
    BOX_HEADER: Locator = (By.CSS_SELECTOR, "div#column-{box} header")

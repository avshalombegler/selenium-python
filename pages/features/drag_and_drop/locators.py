"""
Module containing locators for Drag And Drop page object.
"""

from selenium.webdriver.common.by import By


class DragAndDropPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    BOX = (By.CSS_SELECTOR, "div#column-{box}")
    BOX_HEADER = (By.CSS_SELECTOR, "div#column-{box} header")

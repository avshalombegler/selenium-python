"""
Module containing locators for Files Download page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class FilesDownloadPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    FILE_LINK: Locator = (By.CSS_SELECTOR, ".example a")
    FILE_NAME_LINK: Locator = (By.LINK_TEXT, "{file_name}")

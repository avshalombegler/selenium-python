"""
Module containing locators for Files Upload page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class FilesUploadPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    FILE_UPLOAD: Locator = (By.ID, "file-upload")
    UPLOAD_BTN: Locator = (By.ID, "file-submit")
    UPLOAD_BOX: Locator = (By.CSS_SELECTOR, "div[id=drag-drop-upload]")


class FileUploadedPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    UPLOADED_FILE: Locator = (By.ID, "uploaded-files")

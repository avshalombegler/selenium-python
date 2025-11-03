"""
Module containing locators for Challenging DOM page object.
"""

from selenium.webdriver.common.by import By


class ChallengingDomPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    BLUE_BTN = (By.CSS_SELECTOR, "a[class='button']")
    RED_BTN = (By.CSS_SELECTOR, "a[class='button alert']")
    GREEN_BTN = (By.CSS_SELECTOR, "a[class='button success']")
    EDIT_BTN = (By.XPATH, "//tbody//tr['{row_num}']//a[(text()='edit')]")
    DEL_BTN = (By.XPATH, "//tbody//tr['{row_num}']//a[(text()='delete')]")
    TABLE_ROWS = (By.CSS_SELECTOR, "div.row tr")
    TABLE_HEADERS_TEXT = (By.CSS_SELECTOR, "div.example table thead th")
    TABLE_HEAD_TEXT = (By.XPATH, "//th[text()='{column_name}']")
    TABLE_CELL_TEXT = (
        By.XPATH,
        "//th[text()='{column_name}']/ancestor::thead/following::tr//td[text()='{cell_value}']",
    )

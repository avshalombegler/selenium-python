"""
Module containing locators for Selenium page objects.
"""

from selenium.webdriver.common.by import By


class MainPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "h1.heading")
    AB_TESTING_LINK = (By.LINK_TEXT, "A/B Testing")
    ADD_REMOVE_ELEMENTS_LINK = (By.LINK_TEXT, "Add/Remove Elements")
    BASIC_AUTH_LINK = (By.LINK_TEXT, "Basic Auth")
    BROKEN_IMAGES_LINK = (By.LINK_TEXT, "Broken Images")
    CHALLENGING_DOM_LINK = (By.LINK_TEXT, "Challenging DOM")
    CHECKBOXES_LINK = (By.LINK_TEXT, "Checkboxes")
    CONTEXT_MENU_LINK = (By.LINK_TEXT, "Context Menu")
    DIGEST_AUTHENTICATION_LINK = (By.LINK_TEXT, "Digest Authentication")
    DRAG_AND_DROP_LINK = (By.LINK_TEXT, "Drag and Drop")
    DROPDOWN_LINK = (By.LINK_TEXT, "Dropdown")


class AbTestingPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    TITLE = (By.CSS_SELECTOR, "div.example h3")
    CONTENT_PARAGRAPH = (By.CSS_SELECTOR, "div#content p")


class AddRemoveElementsPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div#content h3")
    ADD_ELEMENT_BTN = (By.CSS_SELECTOR, ".example > button")
    DELETE_BTN = (By.CSS_SELECTOR, "#elements > button:first-child")
    DELETE_BTNS = (By.CSS_SELECTOR, "#elements > button")


class BasicAuthPageLocators:
    AUTHORIZED_INDICATOR = (By.CSS_SELECTOR, "div#content p")


class BrokenImagesPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    IMAGES = (By.CSS_SELECTOR, "div.example img")


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


class CheckboxesPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    CHECKBOXES = (By.CSS_SELECTOR, "form#checkboxes input[type='checkbox']")


class ContextMenuPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    HOT_SPOT_BOX = (By.CSS_SELECTOR, "div#hot-spot")


class DigestAuthPageLocators:
    AUTHORIZED_INDICATOR = (By.CSS_SELECTOR, "div#content p")


class DragAndDropPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    BOX = (By.CSS_SELECTOR, "div#column-{box}")
    BOX_HEADER = (By.CSS_SELECTOR, "div#column-{box} header")


class DropdownListPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    DROPDOWN = (By.CSS_SELECTOR, "select#dropdown")
    OPTION = (By.NAME, "{val}")

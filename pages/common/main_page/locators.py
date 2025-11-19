"""
Module containing locators for Main Page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class MainPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "h1.heading")

    AB_TESTING_LINK: Locator = (By.LINK_TEXT, "A/B Testing")
    ADD_REMOVE_ELEMENTS_LINK: Locator = (By.LINK_TEXT, "Add/Remove Elements")
    BROKEN_IMAGES_LINK: Locator = (By.LINK_TEXT, "Broken Images")
    CHALLENGING_DOM_LINK: Locator = (By.LINK_TEXT, "Challenging DOM")
    CHECKBOXES_LINK: Locator = (By.LINK_TEXT, "Checkboxes")
    CONTEXT_MENU_LINK: Locator = (By.LINK_TEXT, "Context Menu")
    DRAG_AND_DROP_LINK: Locator = (By.LINK_TEXT, "Drag and Drop")
    DROPDOWN_LINK: Locator = (By.LINK_TEXT, "Dropdown")
    DYNAMIC_CONTENT_LINK: Locator = (By.LINK_TEXT, "Dynamic Content")
    DYNAMIC_CONTROLS_LINK: Locator = (By.LINK_TEXT, "Dynamic Controls")
    DYNAMIC_LOADING_LINK: Locator = (By.LINK_TEXT, "Dynamic Loading")
    ENTRY_AD_LINK: Locator = (By.LINK_TEXT, "Entry Ad")
    EXIT_INTENT_LINK: Locator = (By.LINK_TEXT, "Exit Intent")
    FILE_DOWNLOAD_LINK: Locator = (By.LINK_TEXT, "File Download")
    FILE_UPLOAD_LINK: Locator = (By.LINK_TEXT, "File Upload")
    FLOATING_MENU_LINK: Locator = (By.LINK_TEXT, "Floating Menu")
    FORM_AUTH_LINK: Locator = (By.LINK_TEXT, "Form Authentication")
    FRAMES_LINK: Locator = (By.LINK_TEXT, "Frames")

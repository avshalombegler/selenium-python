"""
Module containing locators for Main Page object.
"""

from pages.base.base_page import Locator
from selenium.webdriver.common.by import By


class MainPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "h1.heading")

    AB_TESTING_LINK: Locator = (By.LINK_TEXT, "A/B Testing")
    ADD_REMOVE_ELEMENTS_LINK: Locator = (By.LINK_TEXT, "Add/Remove Elements")
    BASIC_AUTH_LINK: Locator = (By.LINK_TEXT, "Basic Auth")
    BROKEN_IMAGES_LINK: Locator = (By.LINK_TEXT, "Broken Images")
    CHALLENGING_DOM_LINK: Locator = (By.LINK_TEXT, "Challenging DOM")
    CHECKBOXES_LINK: Locator = (By.LINK_TEXT, "Checkboxes")
    CONTEXT_MENU_LINK: Locator = (By.LINK_TEXT, "Context Menu")
    DIGEST_AUTHENTICATION_LINK: Locator = (By.LINK_TEXT, "Digest Authentication")
    DRAG_AND_DROP_LINK: Locator = (By.LINK_TEXT, "Drag and Drop")
    DROPDOWN_LINK: Locator = (By.LINK_TEXT, "Dropdown")
    DYNAMIC_CONTENT_LINK: Locator = (By.LINK_TEXT, "Dynamic Content")
    DYNAMIC_CONTROLS_LINK: Locator = (By.LINK_TEXT, "Dynamic Controls")
    DYNAMIC_LOADING_LINK: Locator = (By.LINK_TEXT, "Dynamic Loading")
    ENTRY_AD_LINK: Locator = (By.LINK_TEXT, "Entry Ad")
    EXIT_INTENT_LINK: Locator = (By.LINK_TEXT, "Exit Intent")

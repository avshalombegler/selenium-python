"""
Module containing locators for Main Page object.
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
    DYNAMIC_CONTENT_LINK = (By.LINK_TEXT, "Dynamic Content")
    DYNAMIC_CONTROLS_LINK = (By.LINK_TEXT, "Dynamic Controls")
    DYNAMIC_LOADING_LINK = (By.LINK_TEXT, "Dynamic Loading")
    ENTRY_AD_LINK = (By.LINK_TEXT, "Entry Ad")

from selenium.webdriver.common.by import By


class MainPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "h1.heading")
    AB_TESTING_LINK = (By.LINK_TEXT, "A/B Testing")
    ADD_REMOVE_ELEMENTS_LINK = (By.LINK_TEXT, "Add/Remove Elements")


class AbTestingPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "div.example h3")
    TITLE = (By.CSS_SELECTOR, "div.example h3")
    CONTENT_PARAGRAPH = (By.CSS_SELECTOR, "div#content p")


class AddRemoveElementsPageLocators:
    PAGE_LOADED_INDICATOR = (By.CSS_SELECTOR, "h3")
    ADD_ELEMENT_BTN = (By.CSS_SELECTOR, ".example > button")
    DELETE_BTN = (By.CSS_SELECTOR, "#elements > button:first-child")
    DELETE_BTNS = (By.CSS_SELECTOR, "#elements > button")

"""
Module containing locators for Frames pages object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class FramesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    NESTED_FRAMES_LINK: Locator = (By.LINK_TEXT, "Nested Frames")
    IFRAME_LINK: Locator = (By.LINK_TEXT, "iFrame")


class NestedFramesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, "frameset")
    NESTED_FRAME: Locator = (By.CSS_SELECTOR, "frame[name='frame-{value}']")
    NESTED_FRAME_BODY: Locator = (By.TAG_NAME, "body")


class IframesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = (By.CSS_SELECTOR, ".example h3")
    IFRAME: Locator = (By.CSS_SELECTOR, ".tox-edit-area__iframe")
    RICH_TEXT_AREA: Locator = (By.CSS_SELECTOR, "#tinymce > p")

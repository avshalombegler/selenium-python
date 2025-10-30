from pages.base.base_page import BasePage
from pages.features.dropdown_list_page import DropdownListPage
from utils.locators import MainPageLocators
from pages.features.checkboxes_page import CheckboxesPage
from pages.features.ab_testing_page import ABTestingPage
from pages.features.add_remove_elements_page import AddRemoveElementsPage
from pages.features.basic_auth_page import BasicAuthPage
from pages.features.broken_images_page import BrokenImagesPage
from pages.features.challenging_dom_page import ChallengingDomPage
from pages.features.context_menu_page import ContextMenuPage
from pages.features.digest_auth_page import DigestAuthPage
from pages.features.drag_and_drop_page import DragAndDropPage
from pages.features.dropdown_list_page import DropdownListPage


class MainPage(BasePage):
    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        # self.wait_for_page_to_load(MainPageLocators.PAGE_LOADED_INDICATOR)

    def click_ab_testing(self) -> ABTestingPage:
        self.click_element(MainPageLocators.AB_TESTING_LINK)
        return ABTestingPage(self.driver, self.logger)

    def click_add_remove_elements(self) -> AddRemoveElementsPage:
        self.click_element(MainPageLocators.ADD_REMOVE_ELEMENTS_LINK)
        return AddRemoveElementsPage(self.driver, self.logger)

    def get_basic_auth(self) -> BasicAuthPage:
        return BasicAuthPage(self.driver, self.logger)

    def click_broken_images(self) -> BrokenImagesPage:
        self.click_element(MainPageLocators.BROKEN_IMAGES_LINK)
        return BrokenImagesPage(self.driver, self.logger)

    def click_challenging_dom(self) -> ChallengingDomPage:
        self.click_element(MainPageLocators.CHALLENGING_DOM_LINK)
        return ChallengingDomPage(self.driver, self.logger)

    def click_checkboxes(self) -> CheckboxesPage:
        self.click_element(MainPageLocators.CHECKBOXES_LINK)
        return CheckboxesPage(self.driver, self.logger)

    def click_context_menu(self) -> ContextMenuPage:
        self.click_element(MainPageLocators.CONTEXT_MENU_LINK)
        return ContextMenuPage(self.driver, self.logger)

    def get_digest_auth(self, url) -> DigestAuthPage:
        self.navigate_to(url)
        return DigestAuthPage(self.driver, self.logger)

    def click_drag_and_drop(self) -> DragAndDropPage:
        self.click_element(MainPageLocators.DRAG_AND_DROP_LINK)
        return DragAndDropPage(self.driver, self.logger)

    def click_dropdown_list(self) -> DropdownListPage:
        self.click_element(MainPageLocators.DROPDOWN_LINK)
        return DropdownListPage(self.driver, self.logger)

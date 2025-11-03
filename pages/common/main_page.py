import allure
from pages.base.base_page import BasePage
from utils.locators import MainPageLocators


class MainPage(BasePage):
    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        # self.wait_for_page_to_load(MainPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Navigate to {page_name} page")
    def click_ab_testing_link(self, page_name="A/B Testing"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.AB_TESTING_LINK)
        from pages.features.ab_testing_page import ABTestingPage

        return ABTestingPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_add_remove_elements_link(self, page_name="Add/Remove Elements"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.ADD_REMOVE_ELEMENTS_LINK)
        from pages.features.add_remove_elements_page import AddRemoveElementsPage

        return AddRemoveElementsPage(self.driver, self.logger)

    @allure.step("Returning object of {page_name} page")
    def get_basic_auth_page(self, page_name="Basic Auth"):
        self.logger.info(f"Returning object of {page_name} page.")
        from pages.features.basic_auth_page import BasicAuthPage

        return BasicAuthPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_broken_images_link(self, page_name="Broken Images"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.BROKEN_IMAGES_LINK)
        from pages.features.broken_images_page import BrokenImagesPage

        return BrokenImagesPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_challenging_dom_link(self, page_name="Challenging DOM"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.CHALLENGING_DOM_LINK)
        from pages.features.challenging_dom_page import ChallengingDomPage

        return ChallengingDomPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_checkboxes_link(self, page_name="Checkboxes"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.CHECKBOXES_LINK)
        from pages.features.checkboxes_page import CheckboxesPage

        return CheckboxesPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_context_menu_link(self, page_name="Context Menu"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.CONTEXT_MENU_LINK)
        from pages.features.context_menu_page import ContextMenuPage

        return ContextMenuPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def get_digest_auth_page(self, url, page_name="Digest Authentication"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.navigate_to(url)
        from pages.features.digest_auth_page import DigestAuthPage

        return DigestAuthPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_drag_and_drop_link(self, page_name="Drag and Drop"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.DRAG_AND_DROP_LINK)
        from pages.features.drag_and_drop_page import DragAndDropPage

        return DragAndDropPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_dropdown_list_link(self, page_name="Dropdown List"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.DROPDOWN_LINK)
        from pages.features.dropdown_list_page import DropdownListPage

        return DropdownListPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_dynamic_content_link(self, page_name="Dynamic Content"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.DYNAMIC_CONTENT_LINK)
        from pages.features.dynamic_content_page import DynamicContentPage

        return DynamicContentPage(self.driver, self.logger)

    @allure.step("Return object of {page_name} page")
    def get_dynamic_content_page(self, page_name="Dynamic Content"):
        self.logger.info(f"Returning object of {page_name} page.")
        from pages.features.dynamic_content_page import DynamicContentPage

        return DynamicContentPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_dynamic_controls_link(self, page_name="Dynamic Controls"):
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.DYNAMIC_CONTROLS_LINK)
        from pages.features.dynamic_controls_page import DynamicControlsPage

        return DynamicControlsPage(self.driver, self.logger)

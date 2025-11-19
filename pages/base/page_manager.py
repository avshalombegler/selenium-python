from __future__ import annotations
from typing import TYPE_CHECKING
import allure
from pages.common.main_page.main_page import MainPage
from pages.common.main_page.locators import MainPageLocators
from pages.features.ab_testing.ab_testing_page import ABTestingPage
from pages.features.add_remove_elements.add_remove_elements_page import AddRemoveElementsPage
from pages.features.basic_auth.basic_auth_page import BasicAuthPage
from pages.features.broken_images.broken_images_page import BrokenImagesPage
from pages.features.challenging_dom.challenging_dom_page import ChallengingDomPage
from pages.features.checkboxes.checkboxes_page import CheckboxesPage
from pages.features.context_menu.context_menu_page import ContextMenuPage
from pages.features.digest_auth.digest_auth_page import DigestAuthPage
from pages.features.drag_and_drop.drag_and_drop_page import DragAndDropPage
from pages.features.dropdown_list.dropdown_list_page import DropdownListPage
from pages.features.dynamic_content.dynamic_content_page import DynamicContentPage
from pages.features.dynamic_controls.dynamic_controls_page import DynamicControlsPage
from pages.features.dynamic_loading.dynamic_loading_page import DynamicLoadingPage
from pages.features.entry_ad.entry_ad_page import EntryAdPage
from pages.features.exit_intent.exit_intent_page import ExitIntentPage
from pages.features.files_download.files_download_page import FilesDownloadPage
from pages.features.files_upload.files_upload_page import FileUploadPage
from pages.features.floating_menu.floating_menu_page import FloatingMenuPage
from pages.features.form_authentication.form_authentication_page import FormAuthenticationPage
from utils.logging_helper import get_logger

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from logging import Logger


class PageManager:
    def __init__(self, driver: WebDriver, logger: Logger | None = None) -> None:
        self.driver = driver
        # Use the provided logger or obtain the configured root logger so
        # all pages built by PageManager share the same logger instance.
        self.logger = logger if logger is not None else get_logger(__name__)
        self.main_page = MainPage(driver, self.logger)

    @allure.step("Navigate to base URL: {url}")
    def navigate_to_base_url(self, url: str) -> MainPage:
        self.main_page.navigate_to(url)
        self.main_page.wait_for_page_to_load(MainPageLocators.PAGE_LOADED_INDICATOR)
        return self.main_page

    def get_ab_testing_page(self) -> ABTestingPage:
        return self.main_page.click_ab_testing_link()

    def get_add_remove_elements_page(self) -> AddRemoveElementsPage:
        return self.main_page.click_add_remove_elements_link()

    def get_basic_auth_page(self) -> BasicAuthPage:
        return self.main_page.get_basic_auth_page()

    def get_broken_images_page(self) -> BrokenImagesPage:
        return self.main_page.click_broken_images_link()

    def get_challenging_dom_page(self) -> ChallengingDomPage:
        return self.main_page.click_challenging_dom_link()

    def get_checkboxes_page(self) -> CheckboxesPage:
        return self.main_page.click_checkboxes_link()

    def get_context_menu_page(self) -> ContextMenuPage:
        return self.main_page.click_context_menu_link()

    def get_digest_auth_page(self, username: str, password: str) -> DigestAuthPage:
        if not username or not password:
            raise ValueError(f"Invalid credentials: username='{username}', password='{password or ''}'")
        url = f"https://{username}:{password}@the-internet.herokuapp.com/digest_auth"
        return self.main_page.get_digest_auth_page(url)

    def get_drag_and_drop_page(self) -> DragAndDropPage:
        return self.main_page.click_drag_and_drop_link()

    def get_dropdown_list_page(self) -> DropdownListPage:
        return self.main_page.click_dropdown_list_link()

    def get_dynamic_content_page(self) -> DynamicContentPage:
        return self.main_page.click_dynamic_content_link()

    def get_dynamic_controls_page(self) -> DynamicControlsPage:
        return self.main_page.click_dynamic_controls_link()

    def get_dynamic_loading_page(self) -> DynamicLoadingPage:
        return self.main_page.click_dynamic_loading_link()

    def get_entry_ad_page(self) -> EntryAdPage:
        return self.main_page.click_entry_ad_link()

    def get_exit_intent_page(self) -> ExitIntentPage:
        return self.main_page.click_exit_intent_link()

    def get_file_download_page(self) -> FilesDownloadPage:
        return self.main_page.click_file_download_link()

    def get_file_upload_page(self) -> FileUploadPage:
        return self.main_page.click_file_upload_link()

    def get_floating_menu_page(self) -> FloatingMenuPage:
        return self.main_page.click_floating_menu_link()

    def get_form_authentication_page(self) -> FormAuthenticationPage:
        return self.main_page.click_form_authentication_link()

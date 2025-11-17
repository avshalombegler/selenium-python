from __future__ import annotations
from typing import TYPE_CHECKING
import allure
import time
from pages.base.base_page import BasePage
from pages.features.drag_and_drop.locators import DragAndDropPageLocators

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.common.action_chains import ActionChains
    from logging import Logger


class DragAndDropPage(BasePage):
    """Page object for the Drag and Drop page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: WebDriver, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(DragAndDropPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get box element")
    def get_box_element(self, box: str) -> WebElement:
        locator = DragAndDropPageLocators.BOX[1].format(box=box)
        return self.wait_for_visibility((DragAndDropPageLocators.BOX[0], locator))

    @allure.step("Perform drag and drop on box")
    def drag_and_drop_box(self, actions: ActionChains, source: WebElement, target: WebElement) -> None:
        # Check if the driver is Firefox; if so, skip ActionChains and use JS directly
        is_firefox = "firefox" in self.driver.name.lower()

        if not is_firefox:
            try:
                # Try ActionChains first for Chrome/other browsers
                actions.drag_and_drop(source, target).perform()
                self.logger.info("Drag and drop completed using ActionChains.")
                time.sleep(0.4)  # Allow DOM update
                return
            except Exception as e:
                self.logger.warning(f"ActionChains drag_and_drop failed: {e}. Falling back to JS.")

        # Fallback to improved JS simulation for Firefox or if ActionChains failed
        self._js_drag_and_drop(source, target)

    def _js_drag_and_drop(self, source: WebElement, target: WebElement) -> None:
        """Improved JS-based drag and drop simulation using HTML5 events."""
        js = """
        function simulateHTML5DragDrop(source, target) {
            // Create a DataTransfer object if supported, else a simple mock
            var dataTransfer = null;
            try {
                dataTransfer = new DataTransfer();
            } catch (e) {
                dataTransfer = {
                    data: {},
                    setData: function(key, val) { this.data[key] = val; },
                    getData: function(key) { return this.data[key]; },
                    effectAllowed: 'move',
                    dropEffect: 'move'
                };
            }
            // Dispatch dragstart on source
            var dragStartEvent = new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            source.dispatchEvent(dragStartEvent);
            // Dispatch dragenter and dragover on target to prepare for drop
            var dragEnterEvent = new DragEvent('dragenter', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            target.dispatchEvent(dragEnterEvent);
            var dragOverEvent = new DragEvent('dragover', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            target.dispatchEvent(dragOverEvent);
            // Dispatch drop on target
            var dropEvent = new DragEvent('drop', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            target.dispatchEvent(dropEvent);
            // Dispatch dragend on source
            var dragEndEvent = new DragEvent('dragend', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            source.dispatchEvent(dragEndEvent);
        }
        simulateHTML5DragDrop(arguments[0], arguments[1]);
        """
        try:
            self.driver.execute_script(js, source, target)
            self.logger.info("Drag and drop completed using JS simulation.")
        except Exception as e:
            self.logger.error(f"JS drag_and_drop failed: {e}")
            raise
        time.sleep(0.4)  # Allow DOM update

    @allure.step("Get box header")
    def get_box_header(self, box: str) -> str:
        locator = DragAndDropPageLocators.BOX_HEADER[1].format(box=box)
        return self.get_dynamic_element_text((DragAndDropPageLocators.BOX_HEADER[0], locator))

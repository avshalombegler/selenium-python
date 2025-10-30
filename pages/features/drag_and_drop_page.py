import allure
import time
from pages.base.base_page import BasePage
from utils.locators import DragAndDropPageLocators


class DragAndDropPage(BasePage):
    """Page object for the Drag and Drop page containing methods to interact with and validate page functionality"""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait_for_page_to_load(DragAndDropPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get box element")
    def get_box_element(self, box):
        self.logger.info("Get box element.")
        locator = DragAndDropPageLocators.BOX[1].format(box=box)
        return self.wait_for_visibility((DragAndDropPageLocators.BOX[0], locator))

    @allure.step("Perform drag and drop on box")
    def drag_and_drop_box(self, actions, source, target):
        self.logger.info("Perform drag and drop on box.")
        try:
            # Try ActionChains first
            actions.drag_and_drop(source, target).perform()
        except Exception as e:
            # Fallback to an HTML5 JS-based drag/drop if ActionChains fails
            self.logger.warning(f"ActionChains drag_and_drop failed: {e}. Falling back to JS HTML5 drag-and-drop.")
            js = (
                "function simulateDragDrop(source, target) {"
                "  var dataTransfer = { data: {}, setData: function(k,v){this.data[k]=v;}, getData: function(k){return this.data[k];} };"
                "  function emit(el, type) {"
                "    var evt = document.createEvent('CustomEvent');"
                "    evt.initCustomEvent(type, true, true, null);"
                "    evt.dataTransfer = dataTransfer;"
                "    el.dispatchEvent(evt);"
                "  }"
                "  emit(source, 'dragstart');"
                "  emit(target, 'drop');"
                "  emit(source, 'dragend');"
                "}"
                "simulateDragDrop(arguments[0], arguments[1]);"
            )
            try:
                self.driver.execute_script(js, source, target)
            except Exception as e2:
                self.logger.error(f"JS drag_and_drop fallback failed: {e2}")
                raise
        # Small pause to allow DOM update; get_box_header uses waits but extra safety helps
        time.sleep(0.4)
        
    @allure.step("Get box header")
    def get_box_header(self, box):
        self.logger.info("Get box header.")
        locator = DragAndDropPageLocators.BOX_HEADER[1].format(box=box)
        return self.get_dynamic_element_text((DragAndDropPageLocators.BOX_HEADER[0], locator))

import allure
import requests
from pages.base_page import BasePage
from utils.locators import BasicAuthPageLocators
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)


class BasicAuth(BasePage):
    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)

    @allure.step(".")
    def init_url(self, username, password):
        self.logger.info(".")
        if username == "" and password == "":
            return "http://the-internet.herokuapp.com/basic_auth"
        else:
            return f"http://{username}:{password}@the-internet.herokuapp.com/basic_auth"

    @allure.step(".")
    def navigate_using_url(self, url):
        self.logger.info(".")
        self.navigate_to(url)

    @allure.step("Get authorization message.")
    def get_auth_message(self):
        self.logger.info("Attempting to get authorization message.")
        try:
            message = self.get_dynamic_element_text(BasicAuthPageLocators.AUTHORIZED_INDICATOR)
            return message
        except (NoSuchElementException, TimeoutException):
            try:
                url = "http://the-internet.herokuapp.com/basic_auth"
                response = requests.get(url)
                if response.status_code == 401:
                    return response.text
                else:
                    raise ValueError(f"Unexpected HTTP status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                raise ValueError(f"Failed to get HTTP response: {e}")

import allure
import requests
from pages.base.base_page import BasePage
from utils.locators import BasicAuthPageLocators
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)


class BasicAuthPage(BasePage):
    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)

    @allure.step("Initialize URL based on username and password")
    def init_url(self, username, password):
        self.logger.info("Initialize URL based on username and password.")
        if username == "" and password == "":
            return self.base_url + "basic_auth"
        else:
            return f"http://{username}:{password}@the-internet.herokuapp.com/basic_auth"

    @allure.step("Navigate to URL: {url}")
    def navigate_using_url(self, url):
        self.logger.info("Navigate to URL: {url}.")
        self.navigate_to(url)

    @allure.step("Get authorization message")
    def get_auth_message(self):
        self.logger.info("Get authorization message.")
        try:
            message = self.get_dynamic_element_text(BasicAuthPageLocators.AUTHORIZED_INDICATOR)
            return message
        except (NoSuchElementException, TimeoutException):
            try:
                url = self.base_url + "basic_auth"
                response = requests.get(url)
                if response.status_code == 401:
                    return response.text
                else:
                    raise ValueError(f"Unexpected HTTP status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                raise ValueError(f"Failed to get HTTP response: {e}")

import logging
import traceback
import sys

sys.path.append('.')
from utils.BaseSelenium import BaseSelenium
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver.support.select import Select


class BasePage(object):
    WEB_DRIVER = BaseSelenium().driver
    default_timeout = 10

    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def open_url(self, url: str):
        try:
            self.WEB_DRIVER.set_page_load_timeout(10)
            self.WEB_DRIVER.implicitly_wait(5)
            self.WEB_DRIVER.get(url)
            self.WEB_DRIVER.maximize_window()
        except Exception:
            self.logger.debug(traceback.format_exc())

    def find_element(self, locator: tuple[str, str]):
        try:
            return self.WEB_DRIVER.find_element(*locator)
        except Exception:
            self.logger.debug(traceback.format_exc())

    def find_elements(self, locator: tuple[str, str]):
        try:
            return self.WEB_DRIVER.find_elements(*locator)
        except Exception:
            self.logger.debug(traceback.format_exc())

    def select_value_from_list(self, list_locator: tuple[str, str], value: str):
        try:
            self.wait_for_element_to_be_visible(list_locator)
            dropdown = Select(self.find_element(list_locator))
            dropdown.select_by_value(value)
            self.logger.debug(f"Element {value} selected")
        except Exception:
            self.logger.debug(traceback.format_exc())

    def click_element(self, locator: tuple[str, str], timeout: float = default_timeout):
        try:
            wait_for_element = WebDriverWait(self.WEB_DRIVER, timeout)
            element = wait_for_element.until(EC.all_of(
                EC.visibility_of_element_located(locator),
                EC.element_to_be_clickable(locator)
            ))

            action = ActionChains(self.WEB_DRIVER)
            action.click(element[0])
            action.perform()
            self.logger.debug(f"Element with locator {locator} clicked")
        except Exception:
            self.logger.debug(traceback.format_exc())

    def click_element_with_javascript(self, locator: tuple[str, str], timeout: float = default_timeout):
        try:
            wait_for_element = WebDriverWait(self.WEB_DRIVER, timeout)
            element = wait_for_element.until(EC.element_to_be_clickable(locator))
            self.WEB_DRIVER.execute_script("arguments[0].click();", element)
            self.logger.debug(f"Element with locator {locator} clicked")
        except Exception:
            self.logger.debug(traceback.format_exc())

    def wait_for_element_to_be_visible(self, locator: tuple[str, str], timeout: float = default_timeout):
        try:
            wait_for_element = WebDriverWait(self.WEB_DRIVER, timeout)
            wait_for_element.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            self.logger.debug(traceback.format_exc())

    def input_text(self, locator: tuple[str, str], value: str, timeout: float = default_timeout):
        try:
            wait_for_element = WebDriverWait(self.WEB_DRIVER, timeout)
            element = wait_for_element.until(EC.element_to_be_clickable(locator))
            action = ActionChains(self.WEB_DRIVER)
            action.click(element)
            action.key_down(Keys.CONTROL)
            action.send_keys("a")
            action.key_up(Keys.CONTROL)
            action.send_keys(value)
            action.perform()
            self.logger.debug(f"Text {value} typed in element {locator}")
        except TimeoutException:
            self.logger.debug(traceback.format_exc())

    def is_element_present(self, locator: tuple[str, str], timeout: float = default_timeout):
        try:
            wait_for_element = WebDriverWait(self.WEB_DRIVER, timeout, ignored_exceptions=(ElementNotVisibleException))
            return wait_for_element.until(EC.presence_of_element_located(locator))
        except Exception:
            self.logger.debug(traceback.format_exc())

    def scroll_to_element(self, locator: tuple[str, str], timeout: float = default_timeout):
        try:
            if self.is_element_present(locator):
                wait_for_element = WebDriverWait(self.WEB_DRIVER, timeout)
                element = wait_for_element.until(EC.presence_of_element_located(locator))
                action = ActionChains(self.WEB_DRIVER)
                action.scroll_to_element(element)
                action.perform()
        except Exception:
            self.logger.debug(traceback.format_exc())

    def teardown(self):
        self.WEB_DRIVER.quit()

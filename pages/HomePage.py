from pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    BUTTON_ACCEPT_COOKIES = (By.CSS_SELECTOR, "[data-testid='Accept all-btn']:nth-child(2)")
    BUTTON_CONTINUE = (By.CSS_SELECTOR, "[data-testid='onsite-messaging-unit-complianceBlockerCard'] button")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "[data-testid='search-button']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-testid='search-input']")
    SEARCH_GO_BUTTON = (By.CSS_SELECTOR, "[data-testid='search-submit']")

    def __init__(self):
        super().__init__()

    def open_site(self, url: str):
        self.open_url(url)
        self.click_element(self.BUTTON_ACCEPT_COOKIES)
        self.click_element(self.BUTTON_CONTINUE)

    def click_search_button(self):
        self.click_element(self.SEARCH_BUTTON)

    def search_text(self, text_to_search: str):
        self.click_element(self.SEARCH_INPUT)
        self.input_text(self.SEARCH_INPUT, value=text_to_search)
        self.click_element(self.SEARCH_GO_BUTTON)

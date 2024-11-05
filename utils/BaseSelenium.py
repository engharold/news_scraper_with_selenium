from selenium import webdriver


class BaseSelenium:
    def __init__(self):
        self.driver = webdriver.Chrome()

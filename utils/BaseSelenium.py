# from RPA.Browser.Selenium import Selenium
#
# class ExtendedSelenium(Selenium):
#
#     def __init__(self, *args, **kwargs):
#         Selenium.__init__(self, *args, **kwargs)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseSelenium:
    def __init__(self):
        self.driver = webdriver.Chrome()

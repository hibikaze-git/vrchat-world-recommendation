import os
import time

import chromedriver_binary

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class AjaxTests(TestCase):
    """
    Chrome上でajaxのテストを行う
    """
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size('1920', '1080')

        self.username = os.environ.get('TEST_USER_NAME')
        self.password = os.environ.get('TEST_USER_PASS')

    def test_login(self):
        self.driver.get("http://localhost:8000/")
        time.sleep(2)

        login_check(self.driver, self.username, self.password)


def login_check(driver, username, password):
    if len(driver.find_elements(By.LINK_TEXT, "ログアウト")) < 1:
        driver.find_element(By.LINK_TEXT, "ログイン").click()
        time.sleep(2)

        user_name_box = driver.find_element(By.ID, "id_username")
        user_name_box.send_keys(username)

        pass_box = driver.find_element(By.ID, "id_password")
        pass_box.send_keys(password)

        driver.find_element(By.ID, "id_submit").click()
        time.sleep(2)

        if len(driver.find_elements(By.LINK_TEXT, "ログアウト")) < 1:
            raise

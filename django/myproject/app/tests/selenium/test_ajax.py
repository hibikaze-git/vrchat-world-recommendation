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

    def login_check(self):
        if len(self.driver.find_elements(By.LINK_TEXT, "ログアウト")) < 1:
            self.driver.find_element(By.LINK_TEXT, "ログイン").click()
            time.sleep(1)

            user_name_box = self.driver.find_element(By.ID, "id_username")
            user_name_box.send_keys(self.username)

            pass_box = self.driver.find_element(By.ID, "id_password")
            pass_box.send_keys(self.password)

            self.driver.find_element(By.ID, "id_submit").click()
            time.sleep(1)

            if len(self.driver.find_elements(By.LINK_TEXT, "ログアウト")) < 1:
                raise

    def test_login(self):
        self.driver.get("http://localhost:8000/")
        time.sleep(1)

        self.login_check()

    def test_visit(self):
        self.driver.get("http://localhost:8000/")
        time.sleep(1)

        self.login_check()

        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_name = visit_btn.get_attribute("title")
        self.assertEqual(visit_btn_name, "未訪問")

        visit_btn.click()
        time.sleep(1)

        self.driver.refresh()
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_name = visit_btn.get_attribute("title")
        self.assertEqual(visit_btn_name, "訪問済み")

        visit_btn.click()
        time.sleep(1)

        self.driver.refresh()
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_name = visit_btn.get_attribute("title")
        self.assertEqual(visit_btn_name, "未訪問")

    def test_like(self):
        self.driver.get("http://localhost:8000/")
        time.sleep(1)

        self.login_check()

        like_btn = self.driver.find_element(By.ID, "like")
        like_btn.click()
        time.sleep(1)

        self.driver.refresh()
        category_new_btn = self.driver.find_element(By.ID, "category-new")
        category_new_btn_title = category_new_btn.get_attribute("title")
        self.assertEqual(category_new_btn_title, "カテゴリ追加")

        like_btn = self.driver.find_element(By.ID, "like")
        like_btn.click()
        time.sleep(1)

        self.driver.refresh()
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn_title = like_btn.get_attribute("title")
        self.assertEqual(like_btn_title, "お気に入りに登録")

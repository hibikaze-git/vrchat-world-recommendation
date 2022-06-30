import os
import time

import chromedriver_binary

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


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

    def create_visit(self):
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_name = visit_btn.get_attribute("title")
        self.assertEqual(visit_btn_name, "未訪問")

        visit_btn.click()
        time.sleep(1)

    def delete_visit(self):
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_name = visit_btn.get_attribute("title")
        self.assertEqual(visit_btn_name, "訪問済み")

        visit_btn.click()

    def create_like(self):
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn.click()
        time.sleep(1)

    def delete_like(self):
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn.click()
        time.sleep(1)

    def create_category(self):
        category_new_btn = self.driver.find_element(By.ID, "category-new")
        category_new_btn_title = category_new_btn.get_attribute("title")
        self.assertEqual(category_new_btn_title, "カテゴリ追加")

        # カテゴリを新規に登録できるか
        category_new_btn.click()
        time.sleep(1)

        new_category = self.driver.find_element(By.NAME, "new-category")
        new_category.send_keys("test-category")
        self.driver.find_element(By.ID, "create-category").click()

        time.sleep(1)

    def delete_category(self):
        self.driver.find_element(By.ID, "category-edit").click()

        time.sleep(1)

        self.driver.find_element(By.ID, "delete-category").click()

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

        # likeボタンが機能するか
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn.click()
        time.sleep(1)

        self.driver.refresh()
        category_new_btn = self.driver.find_element(By.ID, "category-new")
        category_new_btn_title = category_new_btn.get_attribute("title")
        self.assertEqual(category_new_btn_title, "カテゴリ追加")

        # カテゴリの新規登録状態から戻れるか
        category_new_btn.click()
        time.sleep(1)

        back_btn = self.driver.find_element(By.ID, "back-category")
        back_btn_title = back_btn.get_attribute("title")
        self.assertEqual(back_btn_title, "戻る")

        back_btn.click()
        time.sleep(1)

        self.driver.refresh()
        category_new_btn = self.driver.find_element(By.ID, "category-new")
        category_new_btn_title = category_new_btn.get_attribute("title")
        self.assertEqual(category_new_btn_title, "カテゴリ追加")

        # カテゴリを新規に登録できるか
        category_new_btn.click()
        time.sleep(1)

        new_category = self.driver.find_element(By.NAME, "new-category")
        new_category.send_keys("test-category")
        self.driver.find_element(By.ID, "create-category").click()

        time.sleep(1)

        dropdown = self.driver.find_element(By.ID, "category-dropdown")
        select = Select(dropdown)
        selected = select.first_selected_option
        self.assertEqual(selected.text, "test-category")

        time.sleep(1)

        # カテゴリを変更可能か
        select.select_by_visible_text("-")

        time.sleep(1)
        self.driver.refresh()

        dropdown = self.driver.find_element(By.ID, "category-dropdown")
        select = Select(dropdown)
        selected = select.first_selected_option
        self.assertEqual(selected.text, "-")

        # カテゴリを編集可能か
        select.select_by_visible_text("test-category")

        time.sleep(1)
        self.driver.refresh()

        self.driver.find_element(By.ID, "category-edit").click()

        time.sleep(1)

        edit_category = self.driver.find_element(By.NAME, "edit-category")
        edit_category.send_keys("-edit")
        self.driver.find_element(By.ID, "update-category").click()

        time.sleep(1)

        dropdown = self.driver.find_element(By.ID, "category-dropdown")
        select = Select(dropdown)
        selected = select.first_selected_option
        self.assertEqual(selected.text, "test-category-edit")

        # カテゴリを削除できるか
        self.driver.find_element(By.ID, "category-edit").click()

        time.sleep(1)

        self.driver.find_element(By.ID, "delete-category").click()

        time.sleep(1)
        self.driver.refresh()

        dropdown = self.driver.find_element(By.ID, "category-dropdown")
        select = Select(dropdown)
        selected = select.first_selected_option
        self.assertEqual(selected.text, "-")

        # お気に入りを解除できるか
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn.click()
        time.sleep(1)

        self.driver.refresh()
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn_title = like_btn.get_attribute("title")
        self.assertEqual(like_btn_title, "お気に入りに登録")

    def test_select_count(self):
        self.driver.get("http://localhost:8000/")
        time.sleep(1)

        self.login_check()
        dropdown = self.driver.find_element(By.ID, "list-select-count")
        select = Select(dropdown)
        select.select_by_visible_text("50件")

        time.sleep(3)

        twitter_posts = self.driver.find_elements(By.NAME, "twitter-post")

        self.assertEqual(len(twitter_posts), 50)

    def test_narrow(self):
        self.driver.get("http://localhost:8000/")
        time.sleep(1)

        # お気に入り・訪問済みを作成
        self.login_check()

        self.create_like()
        self.create_visit()
        self.create_category()

        # 絞り込み機能のテスト
        self.driver.find_element(By.ID, "modal-open").click()
        time.sleep(1)

        modal = self.driver.find_element(By.ID, "modal")
        modal_class = modal.get_attribute("class")

        self.assertTrue("active" in modal_class)

        self.driver.find_element(By.ID, "narrow-like").click()
        time.sleep(1)

        twitter_posts = self.driver.find_elements(By.NAME, "twitter-post")
        self.assertEqual(len(twitter_posts), 1)

        self.driver.find_element(By.ID, "narrow-visit").click()
        time.sleep(1)

        twitter_posts = self.driver.find_elements(By.NAME, "twitter-post")
        self.assertEqual(len(twitter_posts), 1)

        self.driver.find_element(By.ID, "narrow-all").click()
        time.sleep(1)

        twitter_posts = self.driver.find_elements(By.NAME, "twitter-post")
        self.assertEqual(len(twitter_posts), 25)

        self.driver.find_element(By.NAME, "narrow-category").click()
        time.sleep(1)
        twitter_posts = self.driver.find_elements(By.NAME, "twitter-post")
        self.assertEqual(len(twitter_posts), 1)

        # お気に入り・訪問済みを削除
        self.driver.refresh()

        self.delete_category()
        self.delete_like()
        self.delete_visit()

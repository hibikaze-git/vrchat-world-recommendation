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
        # seleniumの設定
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size('1920', '1080')

        self.username = os.environ.get('TEST_USER_NAME')
        self.password = os.environ.get('TEST_USER_PASS')

    def login_check(self):
        """
        テストユーザーでログイン
        """
        if len(self.driver.find_elements(By.LINK_TEXT, "ログアウト")) < 1:
            self.driver.find_element(By.LINK_TEXT, "ログイン").click()
            time.sleep(2)

            user_name_box = self.driver.find_element(By.ID, "id_username")
            user_name_box.send_keys(self.username)

            pass_box = self.driver.find_element(By.ID, "id_password")
            pass_box.send_keys(self.password)

            self.driver.find_element(By.ID, "id_submit").click()
            time.sleep(2)

            if len(self.driver.find_elements(By.LINK_TEXT, "ログアウト")) < 1:
                raise Exception("ログインに失敗しました")

    def create_visit(self):
        """
        投稿を訪問済みにする
        """
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_name = visit_btn.get_attribute("title")
        self.assertEqual(visit_btn_name, "未訪問")

        visit_btn.click()
        time.sleep(2)

    def delete_visit(self):
        """
        投稿の訪問済みを解除
        """
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_name = visit_btn.get_attribute("title")
        self.assertEqual(visit_btn_name, "訪問済み")

        visit_btn.click()

    def create_like(self):
        """
        投稿をお気に入りにする
        """
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn.click()
        time.sleep(2)

    def delete_like(self):
        """
        投稿のお気に入りを解除
        """
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn.click()
        time.sleep(2)

    def create_category(self):
        """
        投稿のカテゴリを登録
        """
        category_new_btn = self.driver.find_element(By.ID, "category-new")
        category_new_btn_title = category_new_btn.get_attribute("title")
        self.assertEqual(category_new_btn_title, "カテゴリ追加")

        # カテゴリを新規に登録できるか
        category_new_btn.click()
        time.sleep(2)

        new_category = self.driver.find_element(By.NAME, "new-category")
        new_category.send_keys("test-category")
        self.driver.find_element(By.ID, "create-category").click()

        time.sleep(2)

    def delete_category(self):
        """
        投稿のカテゴリを解除・カテゴリそのものを削除
        """
        self.driver.find_element(By.ID, "category-edit").click()

        time.sleep(2)

        self.driver.find_element(By.ID, "delete-category").click()

    def check_visit_btn_display(self):
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_class = visit_btn.get_attribute("class")
        self.assertTrue("own-display-none" not in visit_btn_class)

    def check_visit_btn_no_display(self):
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_class = visit_btn.get_attribute("class")
        self.assertTrue("own-display-none" in visit_btn_class)

    def test_visit(self):
        """
        訪問済み機能のテスト
        """
        self.driver.get("http://localhost:8000/")
        time.sleep(2)

        self.login_check()

        # 未訪問ボタンを取得
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_name = visit_btn.get_attribute("title")
        self.assertEqual(visit_btn_name, "未訪問")

        # 訪問済みにする
        visit_btn.click()
        time.sleep(2)

        self.driver.refresh()
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_name = visit_btn.get_attribute("title")
        self.assertEqual(visit_btn_name, "訪問済み")

        # 訪問済みを解除
        visit_btn.click()
        time.sleep(2)

        self.driver.refresh()
        visit_btn = self.driver.find_element(By.ID, "visit")
        visit_btn_name = visit_btn.get_attribute("title")
        self.assertEqual(visit_btn_name, "未訪問")

    def test_like(self):
        """
        お気に入り機能のテスト
        """
        self.driver.get("http://localhost:8000/")
        time.sleep(2)

        self.login_check()

        # likeボタンが機能するか
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn.click()
        time.sleep(2)

        self.driver.refresh()
        category_new_btn = self.driver.find_element(By.ID, "category-new")
        category_new_btn_title = category_new_btn.get_attribute("title")
        self.assertEqual(category_new_btn_title, "カテゴリ追加")

        # カテゴリの新規登録状態から戻れるか
        category_new_btn.click()
        time.sleep(2)

        self.check_visit_btn_no_display()

        back_btn = self.driver.find_element(By.ID, "back-category")
        back_btn_title = back_btn.get_attribute("title")
        self.assertEqual(back_btn_title, "戻る")

        back_btn.click()
        time.sleep(2)

        self.driver.refresh()
        category_new_btn = self.driver.find_element(By.ID, "category-new")
        category_new_btn_title = category_new_btn.get_attribute("title")
        self.assertEqual(category_new_btn_title, "カテゴリ追加")

        self.check_visit_btn_display()

        # カテゴリを新規に登録できるか
        category_new_btn.click()
        time.sleep(2)

        self.check_visit_btn_no_display()

        new_category = self.driver.find_element(By.NAME, "new-category")
        new_category.send_keys("test-category")
        self.driver.find_element(By.ID, "create-category").click()

        time.sleep(2)

        self.check_visit_btn_display()

        dropdown = self.driver.find_element(By.ID, "category-dropdown")
        select = Select(dropdown)
        selected = select.first_selected_option
        self.assertEqual(selected.text, "test-category")

        time.sleep(2)

        # カテゴリを変更可能か
        select.select_by_visible_text("-")

        time.sleep(2)
        self.driver.refresh()

        dropdown = self.driver.find_element(By.ID, "category-dropdown")
        select = Select(dropdown)
        selected = select.first_selected_option
        self.assertEqual(selected.text, "-")

        # カテゴリを編集可能か
        select.select_by_visible_text("test-category")

        time.sleep(2)
        self.driver.refresh()

        self.driver.find_element(By.ID, "category-edit").click()

        time.sleep(2)

        self.check_visit_btn_no_display()

        edit_category = self.driver.find_element(By.NAME, "edit-category")
        edit_category.send_keys("-edit")
        self.driver.find_element(By.ID, "update-category").click()

        time.sleep(2)

        self.check_visit_btn_display()

        dropdown = self.driver.find_element(By.ID, "category-dropdown")
        select = Select(dropdown)
        selected = select.first_selected_option
        self.assertEqual(selected.text, "test-category-edit")

        # カテゴリを削除できるか
        self.driver.find_element(By.ID, "category-edit").click()

        time.sleep(2)

        self.driver.find_element(By.ID, "delete-category").click()

        time.sleep(2)
        self.driver.refresh()

        self.check_visit_btn_display()

        dropdown = self.driver.find_element(By.ID, "category-dropdown")
        select = Select(dropdown)
        selected = select.first_selected_option
        self.assertEqual(selected.text, "-")

        # お気に入りを解除できるか
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn.click()
        time.sleep(2)

        self.driver.refresh()
        like_btn = self.driver.find_element(By.ID, "like")
        like_btn_title = like_btn.get_attribute("title")
        self.assertEqual(like_btn_title, "お気に入りに登録")

    def test_select_count(self):
        """
        表示件数変更機能のテスト
        """
        self.driver.get("http://localhost:8000/")
        time.sleep(2)

        self.login_check()
        dropdown = self.driver.find_element(By.ID, "list-select-count")
        select = Select(dropdown)
        select.select_by_visible_text("50件")

        time.sleep(2)

        twitter_posts = self.driver.find_elements(By.NAME, "twitter-post")

        self.assertEqual(len(twitter_posts), 50)

    def test_narrow(self):
        """
        投稿絞り込み表示機能のテスト
        """
        self.driver.get("http://localhost:8000/")
        time.sleep(2)

        # お気に入り・訪問済みを作成
        self.login_check()

        self.create_like()
        self.create_visit()
        self.create_category()

        # 絞り込み機能のテスト
        self.driver.find_element(By.ID, "modal-open").click()
        time.sleep(2)

        modal = self.driver.find_element(By.ID, "modal")
        modal_class = modal.get_attribute("class")

        self.assertTrue("active" in modal_class)

        # お気に入りのみ表示
        self.driver.find_element(By.ID, "narrow-like").click()
        time.sleep(2)

        twitter_posts = self.driver.find_elements(By.NAME, "twitter-post")
        self.assertEqual(len(twitter_posts), 1)

        # 訪問済みのみ表示
        self.driver.find_element(By.ID, "narrow-visit").click()
        time.sleep(2)

        twitter_posts = self.driver.find_elements(By.NAME, "twitter-post")
        self.assertEqual(len(twitter_posts), 1)

        # 全て表示
        self.driver.find_element(By.ID, "narrow-all").click()
        time.sleep(2)

        twitter_posts = self.driver.find_elements(By.NAME, "twitter-post")
        self.assertEqual(len(twitter_posts), 25)

        # カテゴリを指定して絞り込み
        self.driver.find_element(By.NAME, "narrow-category").click()
        time.sleep(2)
        twitter_posts = self.driver.find_elements(By.NAME, "twitter-post")
        self.assertEqual(len(twitter_posts), 1)

        # お気に入り・訪問済みを削除
        self.driver.refresh()

        self.delete_category()
        self.delete_like()
        self.delete_visit()

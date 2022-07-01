from django.test import TestCase
from django.urls import resolve

from ..views.category import *
from ..views.index import *
from ..views.like import *
from ..views.narrow import *
from ..views.twitter_view import update_twitter_post
from ..views.visit import *


# Create your tests here.
class TestUrls(TestCase):
    # index
    def test_index(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, IndexView)

    def test_search_index(self):
        view = resolve('/search_index')
        self.assertEqual(view.func.view_class, IndexSearchView)

    def test_recent(self):
        view = resolve('/twitter/recent/')
        self.assertEqual(view.func, update_twitter_post)

    # like
    def test_like(self):
        view = resolve('/like')
        self.assertEqual(view.func, like_view)

    # visit
    def test_visit(self):
        view = resolve('/visit')
        self.assertEqual(view.func, visit_view)

    # category
    def test_change_category(self):
        view = resolve('/change_category')
        self.assertEqual(view.func, change_category_view)

    def test_new_category(self):
        view = resolve('/new_category')
        self.assertEqual(view.func, new_category_view)

    def test_back_category(self):
        view = resolve('/back_category')
        self.assertEqual(view.func, back_category_view)

    def test_create_category(self):
        view = resolve('/create_category')
        self.assertEqual(view.func, create_category_view)

    def test_edit_category(self):
        view = resolve('/edit_category')
        self.assertEqual(view.func, edit_category_view)

    def test_delete_category(self):
        view = resolve('/delete_category')
        self.assertEqual(view.func, delete_category_view)

    def test_update_category(self):
        view = resolve('/update_category')
        self.assertEqual(view.func, update_category_view)

    # 絞り込み機能
    def test_narrow(self):
        view = resolve('/narrow')
        self.assertEqual(view.func, narrow_view)

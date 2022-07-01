from django.urls import path

from .views.category import *
from .views.index import *
from .views.like import *
from .views.narrow import *
from .views.twitter_view import update_twitter_post
from .views.visit import *

app_name = 'app'

urlpatterns = [
    # トップページ
    path('', IndexView.as_view(), name='index'),

    # 検索
    path('search_index', IndexSearchView.as_view(), name='search_index'),

    # ワールド投稿取得
    path('twitter/recent/', update_twitter_post, name='recent'),

    # お気に入り
    path('like', like_view, name='like'),

    # 訪問済み
    path('visit', visit_view, name='visit'),

    # カテゴリ変更
    path('change_category', change_category_view, name='change_category'),

    # カテゴリ
    # new
    path('new_category', new_category_view, name='new_category'),

    # カテゴリ作成取りやめ
    path('back_category', back_category_view, name='back_category'),

    # create
    path('create_category', create_category_view, name='create_category'),

    # edit
    path('edit_category', edit_category_view, name='edit_category'),

    # delete
    path('delete_category', delete_category_view, name='delete_category'),

    # update
    path('update_category', update_category_view, name='update_category'),

    # モーダル
    path('narrow', narrow_view, name='narrow'),
]

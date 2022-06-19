from django.urls import path
from .views.index import IndexView, LikeView, visit_view, change_category_view, new_category_view, back_category_view, create_category_view, edit_category_view, delete_category_view
from .views.twitter_view import update_twitter_post

app_name = 'app'

urlpatterns = [
    # トップページ
    path('', IndexView.as_view(), name='index'),

    # ワールド投稿取得
    path('twitter/recent/', update_twitter_post, name='recent'),

    # お気に入り
    path('like', LikeView, name='like'),

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
]

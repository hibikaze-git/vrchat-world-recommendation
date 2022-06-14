from django.urls import path
from .views.index import IndexView, LikeView, visit_view
from .views.twitter_view import update_twitter_post

app_name = 'app'

urlpatterns = [
    # トップページ
    path('', IndexView.as_view(), name='index'),

    # ワールド投稿取得
    path('twitter/recent/', update_twitter_post, name='recent'),

    # お気に入り機能
    path('like', LikeView, name='like'),

    # お気に入り機能
    path('visit', visit_view, name='visit'),
]

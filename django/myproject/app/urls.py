from django.urls import path
from .views.index import IndexView
from .views.twitter_view import update_twitter_post

app_name = 'app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('twitter/recent/', update_twitter_post, name='recent'),
]

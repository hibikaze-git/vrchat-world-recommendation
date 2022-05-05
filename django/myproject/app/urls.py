from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('', index.IndexView.as_view(), name='index'),
]
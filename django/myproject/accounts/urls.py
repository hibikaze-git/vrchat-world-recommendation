from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, SignUpSuccessView, UserUpdateView

app_name = 'accounts'

urlpatterns = [
    path('signup/',
         SignUpView.as_view(), name='signup'),

    path('signup_success/',
         SignUpSuccessView.as_view(), name='signup_success'),

    path('login/',
         auth_views.LoginView.as_view(template_name="login.html"), name='login'),

    path('logout/',
         auth_views.LogoutView.as_view(template_name="logout.html"), name='logout'),

    # ユーザー情報を更新
    path('update/<int:pk>/',
         UserUpdateView.as_view(), name='update'),
]

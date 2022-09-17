from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, SignUpSuccessView, UserUpdateView, get_csrf, login_view, logout_view, session_view, whoami_view

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

    # react用
    path('accounts/csrf/', get_csrf, name='react-csrf'),
    path('accounts/login/', login_view, name='react-login'),
    path('accounts/logout/', logout_view, name='react-logout'),
    path('accounts/session/', session_view, name='react-session'),
    path('accounts/whoami/', whoami_view, name='react-whoami'),
]

from django.contrib.auth import views as auth_views
from django.test import TestCase
from django.urls import resolve

from ..models import CustomUser
from ..views import SignUpView, SignUpSuccessView, UserUpdateView, CustomPasswordResetView


# Create your tests here.
class UserUrls(TestCase):
    """
    ユーザー情報関連のURLのテスト
    """
    def test_sign_up(self):
        view = resolve('/signup/')
        self.assertEqual(view.func.view_class, SignUpView)

    def test_sigun_up_success(self):
        view = resolve('/signup_success/')
        self.assertEqual(view.func.view_class, SignUpSuccessView)

    def test_login(self):
        view = resolve('/login/')
        self.assertEqual(view.func.view_class, auth_views.LoginView)

    def test_logout(self):
        view = resolve('/logout/')
        self.assertEqual(view.func.view_class, auth_views.LogoutView)

    def test_update_user(self):
        """
        ユーザー情報を更新するurlをテスト
        """
        user_name = "user"
        email = "user@mail.com"
        password = "usertestcreatepass"

        custom_user = CustomUser(
            username=user_name,
            email=email,
            password=password
        )

        custom_user.save()

        view = resolve(f'/update/{custom_user.pk}/')
        self.assertEqual(view.func.view_class, UserUpdateView)


class PasswordResetUrls(TestCase):
    """
    パスワードリセット用URLのテスト
    """
    def test_reset(self):
        view = resolve('/password_reset/')
        self.assertEqual(view.func.view_class, CustomPasswordResetView)

    def test_done(self):
        view = resolve('/password_reset/done/')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetDoneView)

    def test_confirm(self):
        view = resolve('/reset/0c6692f4-5788-c69c-6289-0513b949bb47/dsaliefunpofidsdk/')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetConfirmView)

    def test_complete(self):
        view = resolve('/reset/done/')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetCompleteView)

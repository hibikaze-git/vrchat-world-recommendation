from django.test import TestCase
from django.urls import resolve
from django.contrib.auth import views as auth_views
from ..views import SignUpView, SignUpSuccessView, UserUpdateView
from ..models import CustomUser
from django.test import Client

# Create your tests here.
class TestUrls(TestCase):

    def test_sign_up(self):
        """
        signupのurlをテスト
        """
        view = resolve('/signup/')
        self.assertEqual(view.func.view_class, SignUpView)

    def test_sigun_up_success(self):
        """
         signup_successのurlをテスト
        """
        view = resolve('/signup_success/')
        self.assertEqual(view.func.view_class, SignUpSuccessView)

    def test_login(self):
        """
         loginのurlをテスト
        """
        view = resolve('/login/')
        self.assertEqual(view.func.view_class, auth_views.LoginView)

    def test_logout(self):
        """
         logoutのurlをテスト
        """
        view = resolve('/logout/')
        self.assertEqual(view.func.view_class, auth_views.LogoutView)

    def test_update_user(self):
        """
         updateのurlをテスト
        """
        user_name = "user"
        email = "user@mail.com"
        password = "usertestcreatepass"

        custom_user = CustomUser()
        custom_user.username = user_name
        custom_user.email = email
        custom_user.password = password

        custom_user.save()

        view = resolve(f'/update/{custom_user.pk}')
        self.assertEqual(view.func.view_class, UserUpdateView)

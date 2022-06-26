from django.test import TestCase
from ..models import CustomUser
from django.test import Client


# Create your tests here.
class SignUpTests(TestCase):
    """
    SignUpViewのテストクラス
    """
    def setUp(self):
        self.client = Client()

    def test_post(self):
        response = self.client.post(
            path='/signup/',
            data={
                "username": "user",
                "email": "user@mail.com",
                "password1": "usertestcreatepass",
                "password2": "usertestcreatepass"
            }
        )

        self.assertRedirects(response, '/signup_success/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)


class LoginTests(TestCase):
    """
    LoginView,LogoutViewのテストクラス
    """
    def setUp(self):
        user_name = "user"
        email = "user@mail.com"
        password = "usertestcreatepass"

        custom_user = CustomUser()
        custom_user.username = user_name
        custom_user.email = email
        custom_user.password = password

        custom_user.save()

        self.client = Client()

    def test_login(self):
        response = self.client.post(
            path='/login/',
            data={
                "username": "user",
                "password": "usertestcreatepass",
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/logout/')

        self.assertEqual(response.status_code, 200)


class UserUpdateTests(TestCase):
    """
    UserUpdateViewのテストクラス
    """
    def setUp(self):
        user_name = "user"
        email = "user@mail.com"
        password = "usertestcreatepass"

        self.custom_user = CustomUser()
        self.custom_user.username = user_name
        self.custom_user.email = email
        self.custom_user.password = password

        self.custom_user.save()

        self.client = Client()
        self.client.force_login(self.custom_user)

    def test_post(self):
        edit_username = "edituser"
        edit_email = "edituser@mail.com"

        response = self.client.post(
            path=f'/update/{self.custom_user.pk}',
            data={
                "username": edit_username,
                "email": edit_email,
            }
        )

        saved_user = CustomUser.objects.all()
        actual_user = saved_user[0]

        self.assertRedirects(response, f'/update/{self.custom_user.pk}', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.assertEqual(actual_user.username, edit_username)
        self.assertEqual(actual_user.email, edit_email)

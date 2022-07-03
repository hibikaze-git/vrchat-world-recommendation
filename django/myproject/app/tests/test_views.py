from django.test import Client, TestCase
from accounts.models import CustomUser


# Create your tests here.
class UpdateTwitterPostTests(TestCase):
    """
    update_twitter_postのテストクラス
    """
    def setUp(self):
        user_name = "user"
        email = "user@mail.com"
        password = "usertestcreatepass"

        custom_user = CustomUser(
            username=user_name,
            email=email,
            password=password
        )

        custom_user.is_staff = True

        custom_user.save()

        self.client = Client()
        self.client.force_login(custom_user)

    def test_fetch_recent_data(self):
        # テスト用にクエリを付与
        response = self.client.get('/twitter/recent/?test=true')

        self.assertRedirects(response, '/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)


class IndexViewTests(TestCase):
    """
    トップページのテスト
    """
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

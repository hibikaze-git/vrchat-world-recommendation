from django.test import TestCase

from ..models import CustomUser


# Create your tests here.
class UserModelTests(TestCase):

    def test_is_empty(self):
        """
        初期状態では何も登録されていないことをチェック
        """
        all_user = CustomUser.objects.all()
        self.assertEqual(all_user.count(), 0)

    def test_saving_and_retrieving(self):
        """
        保存後取り出してデータが一致するかを確認
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

        saved_user = CustomUser.objects.all()
        actual_user = saved_user[0]

        self.assertEqual(actual_user.username, user_name)
        self.assertEqual(actual_user.email, email)

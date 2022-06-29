from django.test import TestCase
from django.test import Client


# Create your tests here.
class UpdateTwitterPostTests(TestCase):
    """
    update_twitter_postのテストクラス
    """
    def setUp(self):
        self.client = Client()

    def test_fetch_recent_data(self):
        response = self.client.get('/twitter/recent/?test=true')

        self.assertRedirects(response, '/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

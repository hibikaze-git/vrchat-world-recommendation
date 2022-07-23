from django.test import Client, TestCase

from accounts.models import CustomUser
from ..models import TwitterPost


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
        # twitter投稿データのサンプル
        author_id = "1234"
        username = "abdc"
        text = "abcd"
        media_urls = "https://pbs.twimg.com/media/FWSGBLuVsAA_fnx"
        emb_html = '<blockquote class="twitter-tweet" align="center">'
        emb_url = "https://publish.twitter.com/oembed?"

        for i in range(100):
            twitter_post = TwitterPost(
                tweet_id=i+1,
                author_id=author_id,
                username=username,
                text=text,
                media_urls=media_urls,
                emb_html=emb_html,
                emb_url=emb_url
            )

            twitter_post.save()

        for i in range(100, 110):
            twitter_post = TwitterPost(
                tweet_id=i+1,
                author_id=author_id,
                username=username,
                text="雨",
                media_urls=media_urls,
                emb_html=emb_html,
                emb_url=emb_url
            )

            twitter_post.save()

        self.client = Client()

    def test_index(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_index_paginate(self):
        response = self.client.get('/?search_word=&paginate_by=50&page=2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get("orderby_records")), 50)

    def test_index_search(self):
        response = self.client.get('/?search_word=雨&paginate_by=50&page=1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get("orderby_records")), 10)

from django.test import TestCase
from ..models import TwitterPost, TwitterLike, TwitterCategory, TwitterVisit
from accounts.models import CustomUser

tweet_id = "1234"
author_id = "1234"
username = "abdc"
text = "abcd"
media_urls = "https://pbs.twimg.com/media/FWSGBLuVsAA_fnx"
emb_html = '<blockquote class="twitter-tweet" align="center">'
emb_url = "https://publish.twitter.com/oembed?"


# Create your tests here.
class TwitterPostTests(TestCase):

    def test_saving_and_retrieving(self):
        """
        保存後取り出してデータが一致するかを確認
        """
        twitter_post = TwitterPost(
            tweet_id=tweet_id,
            author_id=author_id,
            username=username,
            text=text,
            media_urls=media_urls,
            emb_html=emb_html,
            emb_url=emb_url
        )

        twitter_post.save()

        saved = TwitterPost.objects.all()
        actual = saved[0]

        self.assertEqual(actual.tweet_id, tweet_id)
        self.assertEqual(actual.username, username)


class TwitterFeatureTests(TestCase):

    def setUp(self):
        self.twitter_post = TwitterPost(
            tweet_id=tweet_id,
            author_id=author_id,
            username=username,
            text=text,
            media_urls=media_urls,
            emb_html=emb_html,
            emb_url=emb_url
        )

        self.twitter_post.save()

        user_name = "user"
        email = "user@mail.com"
        password = "usertestcreatepass"

        self.custom_user = CustomUser(
            username=user_name,
            email=email,
            password=password,
        )

        self.custom_user.save()

    def test_like(self):
        twitter_like = TwitterLike(
            user=self.custom_user,
            twitter_post=self.twitter_post,
            category=None,
        )

        twitter_like.save()

        saved = TwitterLike.objects.all()
        actual = saved[0]

        self.assertEqual(actual.user, self.custom_user)

    def test_visit(self):
        twitter_visit = TwitterVisit(
            user=self.custom_user,
            twitter_post=self.twitter_post
        )

        twitter_visit.save()

        saved = TwitterVisit.objects.all()
        actual = saved[0]

        self.assertEqual(actual.user, self.custom_user)

    def test_category(self):
        category = "abcd"

        twitter_category = TwitterCategory(
            category=category,
            user=self.custom_user
        )

        twitter_category.save()

        saved = TwitterCategory.objects.all()
        actual = saved[0]

        self.assertEqual(actual.category, category)

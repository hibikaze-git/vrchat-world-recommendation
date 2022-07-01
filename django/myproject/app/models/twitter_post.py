from django.db import models


# Create your models here.
class TwitterPost(models.Model):
    """
    APIから取得したツイッターの投稿を保存
    """
    tweet_id = models.CharField(
        max_length=255,
        unique=True
    )

    author_id = models.CharField(
        max_length=255,
    )

    username = models.CharField(
        max_length=100,
    )

    text = models.TextField()

    media_urls = models.TextField()

    emb_html = models.TextField()

    emb_url = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.text

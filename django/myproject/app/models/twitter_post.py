from django.db import models


# Create your models here.
class TwitterPost(models.Model):

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

    # 作成日時 ※レコードを作成時に自動設定
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新日時 ※レコードを更新時に自動設定
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.text

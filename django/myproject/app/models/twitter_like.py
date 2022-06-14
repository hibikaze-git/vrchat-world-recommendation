from django.db import models
from django.conf import settings
from .twitter_post import TwitterPost
from .twitter_category import TwitterCategory

# Create your models here.
class TwitterLike(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    twitter_post = models.ForeignKey(
        TwitterPost,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        TwitterCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # 作成日時 ※レコードを作成時に自動設定
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新日時 ※レコードを更新時に自動設定
    updated_at = models.DateTimeField(auto_now=True)

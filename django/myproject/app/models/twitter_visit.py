from django.db import models
from django.conf import settings

from .twitter_post import TwitterPost


# Create your models here.
class TwitterVisit(models.Model):
    """
    訪問済みか否かを登録
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    twitter_post = models.ForeignKey(
        TwitterPost,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

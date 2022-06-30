from django.conf import settings
from django.db import models


# Create your models here.
class TwitterCategory(models.Model):
    """
    ツイッター投稿のカテゴリー
    """
    category = models.CharField(
        max_length=100,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.category

from django.db import models
from django.conf import settings


# Create your models here.
class TwitterCategory(models.Model):

    category = models.CharField(
        max_length=100,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # 作成日時 ※レコードを作成時に自動設定
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新日時 ※レコードを更新時に自動設定
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.category

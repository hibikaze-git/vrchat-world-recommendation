from django.db import models


# Create your models here.
class TwitterPost(models.Model):
    
    tweet_id = models.CharField(
        max_length=256,
    )

    author_id = models.CharField(
        max_length=256,
    )

    username = models.CharField(
        max_length=100,
    )

    text = models.TextField()

    media_urls = models.TextField()

    emb_html = models.TextField()

    emb_url = models.TextField()

    def __str__(self) -> str:
        return self.text

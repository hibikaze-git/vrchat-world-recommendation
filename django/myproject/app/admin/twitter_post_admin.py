from django.contrib import admin

# Register your models here.
from ..models.twitter_post import TwitterPost

admin.site.register(TwitterPost)

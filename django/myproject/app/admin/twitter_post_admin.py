from django.contrib import admin

# Register your models here.
from ..models.twitter_post import TwitterPost
from ..models.twitter_category import TwitterCategory

admin.site.register(TwitterPost)
admin.site.register(TwitterCategory)

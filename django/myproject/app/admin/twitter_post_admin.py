from django.contrib import admin

# Register your models here.
from ..models.twitter_post import TwitterPost
from ..models.twitter_category import TwitterCategory
from ..models.twitter_like import TwitterLike

admin.site.register(TwitterPost)
admin.site.register(TwitterCategory)
admin.site.register(TwitterLike)

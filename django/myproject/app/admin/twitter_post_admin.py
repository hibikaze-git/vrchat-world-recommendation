from django.contrib import admin

# Register your models here.
from ..models.twitter_post import TwitterPost
from ..models.twitter_category import TwitterCategory
from ..models.twitter_like import TwitterLike
from ..models.twitter_visit import TwitterVisit

admin.site.register(TwitterPost)
admin.site.register(TwitterCategory)
admin.site.register(TwitterLike)
admin.site.register(TwitterVisit)

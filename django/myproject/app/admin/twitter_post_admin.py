from django.contrib import admin

from ..models import TwitterCategory, TwitterLike, TwitterPost, TwitterVisit

# Register your models here.
admin.site.register(TwitterPost)
admin.site.register(TwitterCategory)
admin.site.register(TwitterLike)
admin.site.register(TwitterVisit)

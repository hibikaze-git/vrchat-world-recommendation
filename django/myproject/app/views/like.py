"""
お気に入り機能のview
"""
from django.shortcuts import get_object_or_404, render

from ..models import TwitterCategory, TwitterLike, TwitterPost


def like_view(request):
    if request.method == "POST":
        twitter_post = get_object_or_404(TwitterPost, pk=request.POST.get("twitter_post_id"))
        user = request.user
        like = TwitterLike.objects.filter(twitter_post=twitter_post, user=user)

        if like.exists():
            like.delete()
        else:
            like.create(twitter_post=twitter_post, user=user)

        context = {
            "twitter_post_id": twitter_post.id,
            "record": twitter_post,
            "liked_list": list(TwitterLike.objects.filter(user=user).values_list("twitter_post", flat=True)),
            "category_objects": TwitterCategory.objects.filter(user=user),
            "liked_objects": TwitterLike.objects.filter(user=user)
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return render(request, template_name="like.html", context=context)
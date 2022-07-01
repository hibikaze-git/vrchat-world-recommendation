"""
訪問済み機能のview
"""
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from ..models import TwitterPost, TwitterVisit


def visit_view(request):
    if request.method == "POST":
        get_id = int(request.POST.get("twitter_post_id").replace("visit_", ""))
        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user
        visited = False
        visit = TwitterVisit.objects.filter(twitter_post=twitter_post, user=user)

        if visit.exists():
            visit.delete()
        else:
            visit.create(twitter_post=twitter_post, user=user)
            visited = True

        context = {
            "twitter_post_id": twitter_post.id,
            "visited": visited,
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(context)

from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.http import JsonResponse

from ..models.twitter_post import TwitterPost
from ..models.twitter_like import TwitterLike


class IndexView(ListView):
    """
    トップページのビュー
    """

    template_name = 'index.html'

    context_object_name = "orderby_records"

    queryset = TwitterPost.objects.order_by("-created_at")

    paginate_by = 18

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["liked_list"] = list(TwitterLike.objects.filter(user=self.request.user.id).values_list("twitter_post", flat=True))

        return context


def LikeView(request):
    if request.method == "POST":
        twitter_post = get_object_or_404(TwitterPost, pk=request.POST.get('twitter_post_id'))
        user = request.user
        liked = False
        like = TwitterLike.objects.filter(twitter_post=twitter_post, user=user)

        if like.exists():
            like.delete()
        else:
            like.create(twitter_post=twitter_post, user=user)
            liked = True

        context = {
            'twitter_id': twitter_post.id,
            'liked': liked,
        }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)

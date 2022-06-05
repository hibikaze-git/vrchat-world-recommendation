from django.shortcuts import render

from django.views.generic import ListView

from ..models.twitter_post import TwitterPost


class IndexView(ListView):
    """
    トップページのビュー
    """

    template_name = 'index.html'

    context_object_name = "orderby_records"

    queryset = TwitterPost.objects.order_by("-created_at")

    paginate_by = 1

"""
トップページのview
"""
from django.views.generic import ListView

from ..models import TwitterCategory, TwitterLike, TwitterPost, TwitterVisit


class IndexView(ListView):
    """
    トップページのビュー
    """

    template_name = "index.html"

    context_object_name = "orderby_records"

    paginate_by = 25

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["liked_list"] = list(TwitterLike.objects.filter(user=self.request.user.id).values_list("twitter_post", flat=True))

        context["visited_list"] = list(TwitterVisit.objects.filter(user=self.request.user.id).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=self.request.user.id)

        context["liked_objects"] = TwitterLike.objects.filter(user=self.request.user.id)

        # クエリ
        if self.request.GET.get("search_word") is not None:
            context["search_word"] = self.request.GET.get("search_word")

        return context

    def get_queryset(self):

        queryset = TwitterPost.objects.order_by("-created_at")

        # 検索クエリがある場合には絞り込む
        if self.request.GET.get("search_word") is not None:
            search_word = self.request.GET.get("search_word")

            if search_word != "":
                queryset = queryset.filter(text__icontains=search_word).order_by("-created_at")

        return queryset


class IndexSearchView(ListView):
    """
    トップページのビュー(検索)
    """

    template_name = "contents.html"

    context_object_name = "orderby_records"

    paginate_by = 25

    # postを有効化
    def post(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") != "XMLHttpRequest":
            raise Exception("不正なアクセスです")

        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["liked_list"] = list(TwitterLike.objects.filter(user=self.request.user.id).values_list("twitter_post", flat=True))

        context["visited_list"] = list(TwitterVisit.objects.filter(user=self.request.user.id).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=self.request.user.id)

        context["liked_objects"] = TwitterLike.objects.filter(user=self.request.user.id)

        # クエリ
        if self.request.POST.get("search_word") is not None:
            context["search_word"] = self.request.POST.get("search_word")

        if self.request.POST.get("range") is not None:
            context["range"] = self.request.POST.get("range")

        if self.request.POST.get("categories") is not None:
            context["categories"] = self.request.POST.get("categories")

        return context

    def get_queryset(self):
        search_word = self.request.POST.get("search_word")
        range = self.request.POST.get("range")
        categories = self.request.POST.get("categories")

        queryset = TwitterPost.objects.order_by("-created_at")

        # 範囲で絞り込む
        if self.request.POST.get("range") is not None or range != "all":

            if range == "like":
                liked_id_list = TwitterLike.objects.filter(user=self.request.user).values_list("twitter_post", flat=True)
                queryset = queryset.filter(pk__in=liked_id_list).order_by("-created_at")

            if range == "visit":
                visited_id_list = TwitterVisit.objects.filter(user=self.request.user).values_list("twitter_post", flat=True)
                queryset = queryset.filter(pk__in=visited_id_list).order_by("-created_at")

        # カテゴリで絞り込む
        if categories != "" and categories is not None:
            categories = categories.split(",")
            category_list = TwitterCategory.objects.filter(pk__in=categories)
            liked_id_list = TwitterLike.objects.filter(user=self.request.user, category__in=category_list).values_list("twitter_post", flat=True)
            queryset = queryset.filter(pk__in=liked_id_list).order_by("-created_at")

        # 検索ワードで絞り込む
        if search_word != "" and search_word is not None:
            queryset = queryset.filter(text__icontains=search_word).order_by("-created_at")

        return queryset

    def get_paginate_by(self, queryset):

        return self.request.POST.get("paginate_by", IndexSearchView.paginate_by)

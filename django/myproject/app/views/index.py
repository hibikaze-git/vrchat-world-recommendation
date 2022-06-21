from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.http import JsonResponse

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.twitter_post import TwitterPost
from ..models.twitter_like import TwitterLike
from ..models.twitter_visit import TwitterVisit
from ..models.twitter_category import TwitterCategory


class IndexView(ListView):
    """
    トップページのビュー
    """

    template_name = 'index.html'

    context_object_name = "orderby_records"

    paginate_by = 15

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["liked_list"] = list(TwitterLike.objects.filter(user=self.request.user.id).values_list("twitter_post", flat=True))

        context["visited_list"] = list(TwitterVisit.objects.filter(user=self.request.user.id).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=self.request.user.id)

        context["liked_objects"] = TwitterLike.objects.filter(user=self.request.user.id)

        if self.request.GET.get('search_word') is not None:
            context["search_word"] = self.request.GET.get('search_word')

        return context

    def get_queryset(self):

        queryset = TwitterPost.objects.order_by("-created_at")

        if self.request.GET.get('search_word') is not None:
            search_word = self.request.GET.get('search_word')

            if search_word != "":
                queryset = queryset.filter(text__icontains=search_word).order_by("-created_at")

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return queryset


class IndexSearchView(ListView):
    """
    トップページのビュー(検索)
    """

    template_name = 'contents.html'

    context_object_name = "orderby_records"

    paginate_by = 15

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["liked_list"] = list(TwitterLike.objects.filter(user=self.request.user.id).values_list("twitter_post", flat=True))

        context["visited_list"] = list(TwitterVisit.objects.filter(user=self.request.user.id).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=self.request.user.id)

        context["liked_objects"] = TwitterLike.objects.filter(user=self.request.user.id)

        if self.request.GET.get('search_word') is not None:
            context["search_word"] = self.request.GET.get('search_word')

        if self.request.POST.get('range') is not None:
            context["range"] = self.request.GET.get('range')

        if self.request.POST.get('categories') is not None:
            context["categories"] = self.request.GET.get('categories')

        return context

    def get_queryset(self):
        search_word = self.request.GET.get('search_word')
        range = self.request.POST.get('range')
        categories = self.request.POST.get('categories')

        queryset = TwitterPost.objects.order_by("-created_at")

        if self.request.POST.get('range') is not None or range != "all":

            if range == "like":
                liked_id_list = TwitterLike.objects.filter(user=self.request.user).values_list("twitter_post", flat=True)
                queryset = queryset.filter(pk__in=liked_id_list).order_by("-created_at")

            if range == "visit":
                visited_id_list = TwitterVisit.objects.filter(user=self.request.user).values_list("twitter_post", flat=True)
                queryset = queryset.filter(pk__in=visited_id_list).order_by("-created_at")

        if categories != "" and categories is not None:
            categories = categories.split(",")
            category_list = TwitterCategory.objects.filter(pk__in=categories)
            liked_id_list = TwitterLike.objects.filter(user=self.request.user, category__in=category_list).values_list("twitter_post", flat=True)
            queryset = queryset.filter(pk__in=liked_id_list).order_by("-created_at")

        if search_word != "" and search_word is not None:
            queryset = queryset.filter(text__icontains=search_word).order_by("-created_at")

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return queryset


def LikeView(request):
    if request.method == "POST":
        twitter_post = get_object_or_404(TwitterPost, pk=request.POST.get('twitter_post_id'))
        user = request.user
        like = TwitterLike.objects.filter(twitter_post=twitter_post, user=user)

        if like.exists():
            like.delete()
        else:
            like.create(twitter_post=twitter_post, user=user)

        context = {
            'twitter_post_id': twitter_post.id,
            'record': twitter_post
        }

        context["liked_list"] = list(TwitterLike.objects.filter(user=user).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=user)

        context["liked_objects"] = TwitterLike.objects.filter(user=user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return render(request, template_name="like.html", context=context)


def visit_view(request):
    if request.method == "POST":
        get_id = int(request.POST.get('twitter_post_id').replace("visit_", ""))
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
            'twitter_post_id': twitter_post.id,
            'visited': visited,
        }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)


def change_category_view(request):
    if request.method == "POST":
        get_id = int(request.POST.get('twitter_post_id').replace("category-select_", ""))
        get_category_id = int(request.POST.get('selected_category_id'))

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user

        like = TwitterLike.objects.filter(twitter_post=twitter_post, user=user).first()

        categories = TwitterCategory.objects.filter(user=user).values_list("id", flat=True)

        if get_category_id not in categories:
            like.category = None
            like.save()
        else:
            like.category = TwitterCategory.objects.filter(user=user, id=get_category_id).first()
            like.save()

        context = {
            'twitter_post_id': twitter_post.id,
            'record': twitter_post
        }

        context["liked_list"] = list(TwitterLike.objects.filter(user=user).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=user)

        context["liked_objects"] = TwitterLike.objects.filter(user=user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return render(request, template_name="category.html", context=context)


def new_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get('twitter_post_id').replace("category-new_", ""))

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)

        context = {
            'twitter_post_id': twitter_post.id,
            'record': twitter_post
        }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return render(request, template_name="category_new.html", context=context)


def back_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get('twitter_post_id'))

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user

        context = {
            'twitter_post_id': twitter_post.id,
            'record': twitter_post
        }

        context["liked_list"] = list(TwitterLike.objects.filter(user=user).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=user)

        context["liked_objects"] = TwitterLike.objects.filter(user=user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return render(request, template_name="category.html", context=context)


def create_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get('twitter_post_id').replace("create-category_", ""))
        new_category_name = request.POST.get('new_category_name')

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user

        exist_check = TwitterCategory.objects.filter(user=user, category=new_category_name).first()

        if exist_check is not None or new_category_name == "":
            raise
        else:
            new_category = TwitterCategory.objects.create(user=user, category=new_category_name)
            twitter_like = TwitterLike.objects.filter(user=user, twitter_post=twitter_post).first()
            twitter_like.category = new_category
            twitter_like.save()

        context = {
            'twitter_post_id': twitter_post.id,
            'record': twitter_post
        }

        context["liked_list"] = list(TwitterLike.objects.filter(user=user).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=user)

        context["liked_objects"] = TwitterLike.objects.filter(user=user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return render(request, template_name="category.html", context=context)


def edit_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get('twitter_post_id'))

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user
        liked = TwitterLike.objects.filter(user=user, twitter_post=twitter_post).first()

        context = {
            'twitter_post_id': twitter_post.id,
            'record': twitter_post,
            'liked': liked
        }

        context["liked_list"] = list(TwitterLike.objects.filter(user=user).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=user)

        context["liked_objects"] = TwitterLike.objects.filter(user=user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return render(request, template_name="category_edit.html", context=context)


def delete_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get('twitter_post_id'))

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user

        liked = TwitterLike.objects.filter(user=user, twitter_post=twitter_post).first()

        delete_category = liked.category

        if delete_category is None or delete_category == "":
            raise
        else:
            delete_category.delete()

        context = {
            'twitter_post_id': twitter_post.id,
            'record': twitter_post
        }

        context["liked_list"] = list(TwitterLike.objects.filter(user=user).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=user)

        context["liked_objects"] = TwitterLike.objects.filter(user=user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return render(request, template_name="category.html", context=context)


def update_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get('twitter_post_id'))
        update_category_name = request.POST.get('update_category_name')

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user

        exist_check = TwitterCategory.objects.filter(user=user, category=update_category_name).first()

        if exist_check is not None or update_category_name == "":
            raise
        else:
            update_category = TwitterLike.objects.filter(user=user, twitter_post=twitter_post).first().category
            update_category.category = update_category_name

            update_category.save()

        context = {
            'twitter_post_id': twitter_post.id,
            'record': twitter_post
        }

        context["liked_list"] = list(TwitterLike.objects.filter(user=user).values_list("twitter_post", flat=True))

        context["category_objects"] = TwitterCategory.objects.filter(user=user)

        context["liked_objects"] = TwitterLike.objects.filter(user=user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return render(request, template_name="category.html", context=context)


def narrow_view(request):
    if request.method == "GET":

        user = request.user

        context = {
            "category_objects": TwitterCategory.objects.filter(user=user)
        }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return render(request, template_name="narrow.html", context=context)

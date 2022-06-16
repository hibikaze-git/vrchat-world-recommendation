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

        return context

    def get_queryset(self):
        queryset = TwitterPost.objects.order_by("-created_at")

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
        }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)

"""
カテゴリ関連機能のview
"""
from django.shortcuts import get_object_or_404, render

from ..models import TwitterCategory, TwitterLike, TwitterPost


def change_category_view(request):
    if request.method == "POST":
        get_id = int(request.POST.get("twitter_post_id"))
        get_category_id = int(request.POST.get("selected_category_id"))

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
            "record": twitter_post,
            "category_objects": TwitterCategory.objects.filter(user=user),
            "liked_objects": TwitterLike.objects.filter(user=user)
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return render(request, template_name="category.html", context=context)


def new_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get("twitter_post_id"))

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)

        context = {
            "record": twitter_post
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return render(request, template_name="category_new.html", context=context)


def back_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get("twitter_post_id"))

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user

        context = {
            "record": twitter_post,
            "category_objects": TwitterCategory.objects.filter(user=user),
            "liked_objects": TwitterLike.objects.filter(user=user)
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return render(request, template_name="category.html", context=context)


def create_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get("twitter_post_id"))
        new_category_name = request.POST.get("new_category_name")

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user

        # カテゴリが存在するかを確認
        exist_check = TwitterCategory.objects.filter(user=user, category=new_category_name).first()

        if exist_check is not None or new_category_name == "":
            raise Exception("既に存在するカテゴリです")
        else:
            new_category = TwitterCategory.objects.create(user=user, category=new_category_name)
            twitter_like = TwitterLike.objects.filter(user=user, twitter_post=twitter_post).first()
            twitter_like.category = new_category
            twitter_like.save()

        context = {
            "record": twitter_post,
            "category_objects": TwitterCategory.objects.filter(user=user),
            "liked_objects": TwitterLike.objects.filter(user=user)
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return render(request, template_name="category.html", context=context)


def edit_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get("twitter_post_id"))

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user
        liked = TwitterLike.objects.filter(user=user, twitter_post=twitter_post).first()

        context = {
            "record": twitter_post,
            "liked": liked
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return render(request, template_name="category_edit.html", context=context)


def delete_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get("twitter_post_id"))

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user

        liked = TwitterLike.objects.filter(user=user, twitter_post=twitter_post).first()

        delete_category = liked.category

        if delete_category is None or delete_category == "":
            raise Exception("存在しないカテゴリです")
        else:
            delete_category.delete()

        context = {
            "record": twitter_post,
            "category_objects": TwitterCategory.objects.filter(user=user),
            "liked_objects": TwitterLike.objects.filter(user=user)
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return render(request, template_name="category.html", context=context)


def update_category_view(request):
    if request.method == "POST":

        get_id = int(request.POST.get("twitter_post_id"))
        update_category_name = request.POST.get("update_category_name")

        twitter_post = get_object_or_404(TwitterPost, pk=get_id)
        user = request.user

        # カテゴリが存在するかを確認
        exist_check = TwitterCategory.objects.filter(user=user, category=update_category_name).first()

        if exist_check is not None or update_category_name == "":
            raise Exception("既に存在するカテゴリです")
        else:
            update_category = TwitterLike.objects.filter(user=user, twitter_post=twitter_post).first().category
            update_category.category = update_category_name

            update_category.save()

        context = {
            "record": twitter_post,
            "category_objects": TwitterCategory.objects.filter(user=user),
            "liked_objects": TwitterLike.objects.filter(user=user)
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return render(request, template_name="category.html", context=context)

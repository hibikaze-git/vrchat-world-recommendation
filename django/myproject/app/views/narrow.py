"""
絞り込み機能のview
"""
from django.shortcuts import render

from ..models import TwitterCategory


def narrow_view(request):
    if request.method == "GET":

        user = request.user

        context = {
            "category_objects": TwitterCategory.objects.filter(user=user)
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return render(request, template_name="narrow.html", context=context)

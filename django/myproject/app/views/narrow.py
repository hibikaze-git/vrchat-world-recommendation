"""
絞り込み機能のview
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import TwitterCategory


@login_required
def narrow_view(request):
    if request.method == "GET":

        user = request.user

        context = {
            "category_objects": TwitterCategory.objects.filter(user=user)
        }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return render(request, template_name="narrow.html", context=context)

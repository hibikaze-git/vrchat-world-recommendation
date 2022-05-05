from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    """
    トップページのビュー
    """

    template_name = 'index.html'

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView

from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import CustomUserCreationForm
from .models import CustomUser


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)


class SignUpSuccessView(TemplateView):
    template_name = "signup_success.html"


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = CustomUser
    fields = ('username', 'email')
    template_name = 'my_page.html'

    def form_valid(self, form):
        user = form.save()
        self.object = user

        messages.info(self.request, "ユーザー情報を更新しました。")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("accounts:update", kwargs={"pk": self.kwargs["pk"]})


# パスワードリセット用メールの作成
class CustomPasswordResetView(PasswordResetView):
    extra_email_context = {
        "protocol": settings.MAIL_PROTOCOL,
        "domain": settings.MAIL_DOMAIN,
        "site_name": settings.MAIL_SITE_NAME
    }

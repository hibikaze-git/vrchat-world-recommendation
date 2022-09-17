import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView

from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

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


# react用
# csrfトークンを発行
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response


# ログイン
@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

    login(request, user)
    return JsonResponse({'detail': 'Successfully logged in.'})


# ログアウト
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out.'})


# ログインしているかを確認
@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'isAuthenticated': True})


# ログインしているユーザー名を取得
def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'username': request.user.username})

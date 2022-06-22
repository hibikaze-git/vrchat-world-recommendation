from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib import messages


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

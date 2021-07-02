from django.db import models
from django.urls.base import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "admin@admin.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                messages.success(request, f"Welcome back {user.first_name}")
                login(self.request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})


def log_out(request):
    messages.info(request, "See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Jiho",
        "last_name": "Ju",
        "email": "jiho@jiho.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            messages.success(self.request, f"Welcome!! {user.first_name}")
            login(self.request, user)
        return super().form_valid(form)


class UserProfileView(DetailView):

    """UserProfileView Definition"""

    model = models.User
    context_object_name = "user_obj"
    template_name = "users/user_profile.html"


class UpdateProfileView(SuccessMessageMixin, UpdateView):

    """UserProfileUpdate View Definition"""

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "superhost",
    )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse("users:profile", kwargs={"pk": pk})
        # return self.request.user.get_absolute_url() => 이렇게 User model에서 get_absolute_url를 정의해서 사용할 수 있당~

# from django.core.paginator import Paginator, EmptyPage
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import models as post_models
from users import mixins as user_mixins


class HomeView(ListView):

    """HomeView Definition"""

    model = post_models.Post
    paginate_by = 10
    paginate_orphans = 5
    ordering = "-created"
    context_object_name = "posts"


def post_detail(request, pk):
    try:
        post = post_models.Post.objects.get(pk=pk)
        return render(request, "posts/detail.html", context={"post": post})
    except post_models.Post.DoesNotExist:
        return redirect("core:home")


class EditPostView(user_mixins.LoggedInOnlyView, UpdateView):

    """EditPostView Definition"""

    model = post_models.Post
    template_name = "posts/post_edit.html"
    fields = (
        "title",
        "content",
    )

    # message를 띄워주기 위함!!
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "Post Updated!")
        return super().post(request, *args, **kwargs)

    # 로그인 사용자가 url을 통해 다른 사용자 post/edit에 들어는 것을 막기 위함
    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if post.author.pk != self.request.user.pk:
            raise Http404()
        return post


""" def all_posts(request):
    page = request.GET.get("page", 1)
    post_list = post_models.Post.objects.all()
    paginator = Paginator(post_list, 10, orphans=5)
    try:
        posts = paginator.page(int(page))
        return render(request, "posts/home.html", context={"posts": posts})
    except EmptyPage:
        return redirect("/") """


""" def all_posts(request):
    page = request.GET.get("page", 1)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    page_count = ceil(post_models.Post.objects.count() / page_size)
    all_posts = post_models.Post.objects.all()[offset:limit]
    return render(
        request,
        "posts/home.html",
        context={
            "posts": all_posts,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    ) """

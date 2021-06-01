# from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.views.generic import ListView
from . import models as post_models


class HomeView(ListView):

    """HomeView Definition"""

    model = post_models.Post
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "posts"


def post_detail(request, pk):
    try:
        post = post_models.Post.objects.get(pk=pk)
        return render(request, "posts/detail.html", context={"post": post})
    except post_models.Post.DoesNotExist:
        return redirect("core:home")


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

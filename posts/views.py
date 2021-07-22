# from django.core.paginator import Paginator, EmptyPage
from django.forms.forms import Form
from django.http.response import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, UpdateView, DetailView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import models as post_models
from .forms import AddPhotoForm, AddPostForm
from users import mixins as user_mixins


class HomeView(ListView):

    """HomeView Definition"""

    model = post_models.Post
    paginate_by = 10
    paginate_orphans = 5
    ordering = "-created"
    context_object_name = "posts"


class AddPostView(user_mixins.LoggedInOnlyView, FormView):

    """AddPostView Definition"""

    template_name = "posts/post_add.html"
    form_class = AddPostForm

    def form_valid(self, form):
        user_pk = self.request.user.pk
        post = form.save(user_pk)
        messages.success(self.request, "Post Uploaded!")
        return redirect(reverse("posts:detail", kwargs={"pk": post.pk}))


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


@login_required
def post_delete(request, pk):

    """Post Delete Definition"""

    try:
        post = post_models.Post.objects.get(pk=pk)
        if post.author.pk != request.user.pk:
            messages.error(request, "Can't delete that post")
        else:
            post.delete()
            messages.success(request, "Post Deleted!")
            return redirect(reverse("core:home"))
    except post_models.Post.DoesNotExist:
        return redirect("core:home")


class PostPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    """RoomPhotosView Definition"""

    model = post_models.Post
    template_name = "posts/post_photos.html"

    # 로그인 사용자가 url을 통해 다른 사용자 post/edit에 들어는 것을 막기 위함
    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if post.author.pk != self.request.user.pk:
            raise Http404()
        return post


@login_required
def delete_photo(request, post_pk, photo_pk):

    """Delete Photo Definition"""

    user = request.user
    try:
        # foreign, manytomany 등과 관련된 필드 및  인스턴스를 삭제하려면 항상 관련 객체가 있는지 체크!!!!
        post = post_models.Post.objects.get(pk=post_pk)
        if post.author.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            post_models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted!")
        return redirect(reverse("posts:photos", kwargs={"pk": post_pk}))
    except post_models.Post.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    """PhotoEditView Definition"""

    model = post_models.Photo
    template_name = "posts/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated!"
    fields = (
        "file",
        "caption",
    )

    def get_success_url(self):
        post_pk = self.kwargs.get("post_pk")
        return reverse("posts:photos", kwargs={"pk": post_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    """AddPhotoView Definition"""

    template_name = "posts/photo_add.html"
    form_class = AddPhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded!")
        return redirect(reverse("posts:photos", kwargs={"pk": pk}))


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

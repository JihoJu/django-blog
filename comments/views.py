from django.http.response import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, UpdateView
from .forms import WriteCommentForm
from .models import Comment
from users import mixins as user_mixins


class WriteCommentView(user_mixins.LoggedInOnlyView, FormView):

    """WriteCommentView Definition"""

    template_name = "comments/comment_write.html"
    form_class = WriteCommentForm

    def form_valid(self, form):
        user_pk = self.request.user.pk
        post_pk = self.kwargs.get("pk")
        form.save(user_pk, post_pk)
        messages.success(self.request, "Comment Uploaded!")
        return redirect(reverse("posts:detail", kwargs={"pk": post_pk}))


class UpdateCommentView(user_mixins.LoggedInOnlyView, UpdateView):

    """Update Comment Definition"""

    model = Comment
    template_name = "comments/comment_edit.html"
    fields = ("comment_text",)
    pk_url_kwarg = "comment_pk"

    def get_success_url(self):
        post_pk = self.kwargs.get("post_pk")
        return reverse("posts:detail", kwargs={"pk": post_pk})

    def post(self, request, *args: str, **kwargs):
        messages.success(self.request, "Comment Updated!")
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        comment = super().get_object(queryset=queryset)
        if comment.author_name.pk != self.request.user.pk:
            raise Http404()
        return comment


@login_required
def comment_delete(request, post_pk, comment_pk):

    """Delete Comment Definition"""

    try:
        comment = Comment.objects.get(pk=comment_pk)
        if comment.author_name.pk != request.user.pk:
            messages.error(request, "Can't delete that comment")
        else:
            comment.delete()
            messages.success(request, "Comment Deleted!")
            return redirect(reverse("posts:detail", kwargs={"pk": post_pk}))
    except Comment.DoesNotExist:
        return redirect(reverse("posts:detail", kwargs={"pk": post_pk}))

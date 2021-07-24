from django import forms
from .models import Comment
from users.models import User
from posts.models import Post


class WriteCommentForm(forms.ModelForm):

    """WriteCommentForm Definition"""

    class Meta:
        model = Comment
        fields = ("comment_text",)

    def save(self, user_pk, post_pk, *args, **kwargs):
        comment = super().save(commit=False)
        author = User.objects.get(pk=user_pk)
        post = Post.objects.get(pk=post_pk)
        comment.author_name = author
        comment.post_name = post
        comment.save()

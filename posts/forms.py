from django import forms
from .models import Photo, Post
from users.models import User


class AddPhotoForm(forms.ModelForm):

    """AddPhotoForm Definition"""

    class Meta:
        model = Photo
        fields = (
            "file",
            "caption",
        )

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        post = Post.objects.get(pk=pk)
        photo.post = post
        photo.save()


class AddPostForm(forms.ModelForm):

    """AddPostForm Definition"""

    class Meta:
        model = Post
        fields = (
            "title",
            "content",
        )

    def save(self, user_pk, *args, **kwargs):
        post = super().save(commit=False)
        author = User.objects.get(pk=user_pk)
        post.author = author
        post.save()
        return post

from django.urls import path
from . import views as post_views

app_name = "posts"

urlpatterns = [
    path("add/", post_views.AddPostView.as_view(), name="add"),
    path("<int:pk>", post_views.post_detail, name="detail"),
    path("<int:pk>/edit/", post_views.EditPostView.as_view(), name="edit"),
    path("<int:pk>/delete/", post_views.post_delete, name="delete"),
    path("<int:pk>/photos/", post_views.PostPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add/", post_views.AddPhotoView.as_view(), name="add-photo"),
    path(
        "<int:post_pk>/photos/<int:photo_pk>/delete/",
        post_views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:post_pk>/photos/<int:photo_pk>/edit/",
        post_views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
]

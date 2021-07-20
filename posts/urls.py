from django.urls import path
from . import views as post_views

app_name = "posts"

urlpatterns = [
    path("<int:pk>", post_views.post_detail, name="detail"),
    path("<int:pk>/edit/", post_views.EditPostView.as_view(), name="edit"),
    path("<int:pk>/photos/", post_views.RoomPhotosView.as_view(), name="photos"),
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

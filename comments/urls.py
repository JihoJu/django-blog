from django.urls import path
from .views import WriteCommentView, UpdateCommentView, comment_delete

app_name = "comments"

urlpatterns = [
    path("<int:pk>/write/", WriteCommentView.as_view(), name="write"),
    path(
        "<int:post_pk>/update/<int:comment_pk>",
        UpdateCommentView.as_view(),
        name="update",
    ),
    path("<int:post_pk>/delete/<int:comment_pk>", comment_delete, name="delete"),
]

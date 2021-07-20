from django.urls import path
from . import views as post_views

app_name = "posts"

urlpatterns = [
    path("<int:pk>", post_views.post_detail, name="detail"),
    path("<int:pk>/edit/", post_views.EditPostView.as_view(), name="edit"),
]

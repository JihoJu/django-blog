from django.db import models
from core import models as core_models
from users import models as user_models
from posts import models as post_models


class Comment(core_models.TimeStampedModel):

    """Comment Model Definition"""

    post_name = models.ForeignKey(
        post_models.Post, related_name="post_comments", on_delete=models.CASCADE
    )
    author_name = models.ForeignKey(
        user_models.User, related_name="author_comments", on_delete=models.CASCADE
    )
    comment_text = models.TextField()

    def __str__(self):
        return self.comment_text

from django.db import models
from core import models as core_models
from users import models as user_models


class Post(core_models.TimeStampedModel):

    """Post Model Definition"""

    author = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.author}"

    # TODO
    def comments_count(self):
        commentCount = self.comments.count()
        return int(commentCount)

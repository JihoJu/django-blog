from datetime import datetime, timedelta, timezone
from django.db import models
from django.urls import reverse
from core import models as core_models
from users import models as user_models


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="post_photos")
    post = models.ForeignKey("Post", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


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

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def created_string(self):
        created_time = datetime.now(tz=timezone.utc) - self.created

        if created_time < timedelta(minutes=1):
            return "방금 전"
        elif created_time < timedelta(hours=1):
            return str(int(created_time.seconds / 60)) + " 분 전"
        elif created_time < timedelta(days=1):
            return str(int(created_time.seconds / 3600)) + " 시간 전"
        else:
            created_time = datetime.now(tz=timezone.utc).date() - self.created.date()
            return str(created_time.days) + " 일 전"

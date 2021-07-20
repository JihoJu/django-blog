from datetime import datetime, timedelta, timezone
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete
from core import models as core_models
from users import models as user_models


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="post_photos")
    post = models.ForeignKey("Post", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


# 사진 delete 이벤트 시 uploads에 존재하는 파일 삭제
@receiver(post_delete, sender=Photo)
def file_delete_action(sender, instance, **kwargs):
    instance.file.delete(False)


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
        # setting.py에서 USE_TZ가 True인 경우 datetime.now()로 써도 무방하다.

        if created_time < timedelta(minutes=1):
            return "방금 전"
        elif created_time < timedelta(hours=1):
            return str(int(created_time.seconds / 60)) + " 분 전"
        elif created_time < timedelta(days=1):
            return str(int(created_time.seconds / 3600)) + " 시간 전"
        else:
            created_time = datetime.now(tz=timezone.utc).date() - self.created.date()
            return str(created_time.days) + " 일 전"

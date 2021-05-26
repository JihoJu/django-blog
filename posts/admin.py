from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):

    """Post Admin Definition"""

    fieldsets = (
        (
            "Post Info",
            {
                "fields": (
                    "author",
                    "title",
                    "content",
                ),
            },
        ),
    )

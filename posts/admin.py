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

    list_display = (
        "title",
        "content",
        "author",
        "comments_count",
    )

    search_fields = ("^author__username",)

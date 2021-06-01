from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    """Comment Admin Definition"""

    fieldsets = (
        (
            "Comment Info",
            {
                "fields": (
                    "post_name",
                    "author_name",
                    "comment_text",
                ),
            },
        ),
    )

    list_display = (
        "comment_text",
        "post_name",
        "author_name",
    )

    search_fields = (
        "^author_name__username",
        "^post_name__title",
    )

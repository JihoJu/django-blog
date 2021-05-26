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
                    "post",
                    "author_name",
                    "comment_text",
                ),
            },
        ),
    )

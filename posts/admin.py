from django.contrib import admin
from django.utils.safestring import mark_safe
from . import models


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):

    """Post Admin Definition"""

    inlines = (PhotoInline,)

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


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"

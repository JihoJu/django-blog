from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "bio",
                    "gender",
                    "superhost",
                ),
            },
        ),
    )

    def user_avatar_thumbnail(self, obj):
        return mark_safe(f'<img width=50px src="{obj.avatar.url}" />')

    user_avatar_thumbnail.short_description = "Thumbnail"

    list_display = (
        "username",
        "user_avatar_thumbnail",
        "email",
        "gender",
        "superhost",
    )

    list_filter = (
        "superhost",
        "gender",
    )
    search_fields = ("^username",)

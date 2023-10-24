from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Subscribe

User = get_user_model()
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "username",
    )
    search_fields = (
        "id",
        "email",
        "username",
    )


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ("author", "user")

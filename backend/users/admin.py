from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscribe

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'last_name',
        'first_name',
        'username',
        'email',
        'password'
    )
    list_editable = ('email', 'password')
    list_filter = (
        'last_name',
        'first_name',
        'username',
        'email',
    )
    search_fields = (
        'id',
        'email',
        'username',
    )


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'user'
    )

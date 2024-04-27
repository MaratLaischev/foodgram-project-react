from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import Follow, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'last_login',
        'date_joined',
        'is_superuser',
        'is_active',
    )
    search_fields = ('id', 'username', 'email')
    list_filter = ('email', 'username', )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'following',
    )
    search_fields = ('id', 'user__name')
    list_filter = ('user',)

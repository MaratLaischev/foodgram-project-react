from django.contrib import admin

from user.models import User


class UserAdmin(admin.ModelAdmin):
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


admin.site.register(User, UserAdmin)

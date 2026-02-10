from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'email',
        'citi',
    )
    list_filter = ('citi',)
    search_fields = ('email',)
    ordering = ('email',)

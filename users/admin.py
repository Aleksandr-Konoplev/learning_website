from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "citi",
    )
    list_filter = ("citi",)
    search_fields = ("email",)

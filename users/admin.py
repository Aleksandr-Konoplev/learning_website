from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "citi",
    )
    list_filter = ("citi",)
    search_fields = ("email",)
    ordering = ("email",)

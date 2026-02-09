from django.contrib import admin

from users.models import User


@admin.register(User)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
    )
    list_filter = ("is_active",)
    search_fields = ("email",)
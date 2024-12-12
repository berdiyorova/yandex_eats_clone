from django.contrib import admin
from apps.accounts.models import UserModel, UserConfirmModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "username", "user_role", "phone_number")
    search_fields = ("id", "first_name", "last_name", "username", "phone_number")
    list_filter = ("user_role", "created_at")



@admin.register(UserConfirmModel)
class ClientConfirmAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "is_confirmed", "created_at")
    search_fields = ("id", "code", "created_at")
    list_filter = ("created_at",)

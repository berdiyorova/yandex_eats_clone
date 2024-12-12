from django.contrib import admin

from apps.client.models import ClientAddress


@admin.register(ClientAddress)
class ClientAddressAdmin(admin.ModelAdmin):
    list_display = ("address", "name", "client")
    search_fields = ("address", "name", "client")
    list_filter = ("created_at", "name", "client")

from django.contrib import admin

from apps.orders.models import OrderModel, OrderItemModel


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("total_amount", "payment_method", "status")
    list_filter = ("created_at", "status", "payment_method")


admin.site.register(OrderItemModel)

from django.db import models

from apps.accounts.models import UserModel
from apps.common.models import BaseModel
from apps.restaurants.models import BranchModel


class PaymentMethod(models.TextChoices):
    CASH = 'CASH', 'CASH'
    CLICK = 'CLICK', 'CLICK'
    PAYME = 'PAYME', 'PAYME'


class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'PENDING'
    ACCEPTED = 'ACCEPTED', 'ACCEPTED'
    IN_PROGRESS = 'IN_PROGRESS', 'IN_PROGRESS'
    DELIVERED = 'DELIVERED', 'DELIVERED'
    CANCELLED = 'CANCELLED', 'CANCELLED'


class OrderModel(BaseModel):
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    payment_method = models.CharField(choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.PENDING)

    client = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='orders', null=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItemModel(BaseModel):
    product_name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='orders/', null=True, blank=True)
    product_measure = models.PositiveSmallIntegerField(null=True, blank=True)
    measure_unit = models.CharField(max_length=10)
    product_price = models.DecimalField(max_digits=10, decimal_places=0)

    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='order_items')

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

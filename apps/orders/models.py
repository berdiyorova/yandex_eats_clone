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
    IN_PROGRESS = 'IN_PROGRESS', 'IN_PROGRESS'
    DELIVERED = 'DELIVERED', 'DELIVERED'
    CANCELLED = 'CANCELLED', 'CANCELLED'


class OrderModel(BaseModel):
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    delivery_address = models.CharField(max_length=255)
    delivery_time = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.PENDING)

    client = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='orders', null=True)
    branch = models.ForeignKey(BranchModel, on_delete=models.SET_NULL, related_name='orders', null=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

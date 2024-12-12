from django.db import models

from apps.accounts.models import UserModel
from apps.common.models import AddressModel


class ClientAddress(AddressModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    home_number = models.CharField(max_length=10, null=True, blank=True)
    door_phone = models.CharField(max_length=20, null=True, blank=True)
    entrance = models.PositiveSmallIntegerField(null=True, blank=True)
    floor = models.PositiveSmallIntegerField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)

    client = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="addresses")

    class Meta:
        verbose_name = 'Client Address'
        verbose_name_plural = 'Client Addresses'
        unique_together = ('address', 'client')

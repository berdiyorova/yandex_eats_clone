from django.db import models

from apps.accounts.models import UserModel
from apps.common.models import AddressModel


class RestaurantModel(AddressModel):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL, related_name="restaurants")
    service_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'


class BranchModel(AddressModel):
    name = models.CharField(max_length=255)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    restaurant = models.ForeignKey(RestaurantModel, on_delete=models.CASCADE, related_name="branches")
    manager = models.OneToOneField(UserModel, null=True, on_delete=models.SET_NULL, related_name="branch")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

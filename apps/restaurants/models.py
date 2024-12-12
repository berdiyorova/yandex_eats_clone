from django.db import models

from apps.accounts.models import UserModel
from apps.common.models import AddressModel


class RestaurantModel(AddressModel):
    name = models.CharField(max_length=255, unique=True)
    manager = models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL, related_name="restaurants")

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'


class BranchModel(AddressModel):
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    restaurant = models.ForeignKey(RestaurantModel, on_delete=models.CASCADE, related_name="branches")
    employee = models.OneToOneField(UserModel, null=True, on_delete=models.SET_NULL, related_name="branch")

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

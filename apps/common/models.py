from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AddressModel(BaseModel):
    longitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('longitude', 'latitude')
        abstract = True

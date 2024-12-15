from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.common.models import BaseModel
from apps.restaurants.models import BranchModel


class MeasureUnit(models.TextChoices):
    g = 'g', 'g'
    ml = 'ml', 'ml'


class CategoryModel(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class IngredientModel(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class ProductModel(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    measure = models.PositiveSmallIntegerField(null=True, blank=True)
    measure_unit = models.CharField(choices=MeasureUnit.choices, default=MeasureUnit.g)
    discount = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    price = models.DecimalField(max_digits=10, decimal_places=0)
    real_price = models.DecimalField(max_digits=10, decimal_places=0)

    category = models.ManyToManyField(CategoryModel, related_name='products')
    branch = models.ManyToManyField(BranchModel, related_name='products')
    ingredients = models.ManyToManyField(IngredientModel, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def is_discount(self):
        return self.discount != 0

from rest_framework import serializers

from apps.products.models import ProductModel


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ('image', 'name', 'real_price', 'measure', 'measure_unit')


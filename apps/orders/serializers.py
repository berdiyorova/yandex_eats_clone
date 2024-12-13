from rest_framework import serializers

from apps.products.models import ProductModel


class ProductSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, default=1)

    class Meta:
        model = ProductModel
        fields = ('image', 'name', 'real_price', 'measure', 'measure_unit', 'quantity')


class OrderItemSerializer(serializers.Serializer):
    serializer = serializers.DictField(child=ProductSerializer())

from rest_framework import serializers

from apps.orders.models import OrderModel
from apps.products.models import ProductModel


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, attrs):
        product_id = attrs.get('product_id')
        product = ProductModel.objects.filter(id=product_id)

        if not product.exists():
            raise serializers.ValidationError("Product does not exists.")

        attrs['price'] = product.first().real_price

        return attrs



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"
        exclude = ('client', 'branch')

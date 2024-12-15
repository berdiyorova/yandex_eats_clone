from rest_framework import serializers

from apps.accounts.models import UserModel, UserRole
from apps.common.utils import calculate_order_total_price, get_nearest_courier
from apps.orders.models import OrderItemModel, PaymentMethod, OrderModel
from apps.products.models import ProductModel


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, attrs):
        product_id = attrs.get('product_id')
        product = ProductModel.objects.filter(id=product_id)

        if not product.exists():
            raise serializers.ValidationError("Product does not exists.")

        return attrs



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemModel
        fields = ('product_name', 'product_image', 'product_measure', 'measure_unit', 'product_price', 'quantity')



class OrderSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=0, read_only=True)
    payment_method = serializers.CharField(default=PaymentMethod.CASH)
    status = serializers.CharField(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = OrderModel
        fields = ('total_amount', 'payment_method', 'status', 'branch', 'order_items')
        read_only_fields = ('branch',)

    def validate(self, data):
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("The request object does not exists")

        cart = request.session.get('cart', [])
        if not cart:
            raise serializers.ValidationError("There are no products in the cart.")
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        cart = request.session.get('cart', [])

        client = request.user
        total_amount = calculate_order_total_price(cart=cart)
        payment_method = validated_data.get('payment_method', PaymentMethod.CASH)

        order = OrderModel.objects.create(
            total_amount=total_amount,
            payment_method=payment_method,
            client=client,
        )

        product = None
        for cart_item in cart:
            product = ProductModel.objects.filter(id=cart_item['product_id']).first()

            OrderItemModel.objects.create(
                product_name=product.name,
                product_image=product.image,
                product_measure=product.measure,
                measure_unit=product.measure_unit,
                product_price=product.real_price,
                quantity=cart_item['quantity'],
                order=order
            )

        order.branch = product.branch
        order.save()
        request.session['cart'] = []

        return order

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.orders.serializers import OrderItemSerializer, ProductSerializer


class CartItemView(GenericAPIView):
    def get(self, request):
        """
        Retrieve the cart items from the session.
        """
        order_items = request.session.get('order_items', {})
        serializer = OrderItemSerializer(data=order_items)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Add or update a product in the cart.
        """
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_data = serializer.validated_data

        order_items = request.session.get('order_items', {})
        order_items[product_data['image']] = product_data
        request.session['order_items'] = order_items

        return Response(order_items, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        """
        Remove a product from the cart.
        """
        order_items = request.session.get('order_items', {})
        if product_id in order_items:
            del order_items[product_id]
            request.session['order_items'] = order_items
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'error': 'Product not found in the cart'},
                status=status.HTTP_404_NOT_FOUND
            )
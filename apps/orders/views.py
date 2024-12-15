from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import IsClient
from apps.orders.serializers import CartItemSerializer


class UserCartView(ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Retrieve the cart",
        responses={200: CartItemSerializer(many=True)}
    )
    def get(self, request):
        """
        Retrieve the cart from the session.
        """
        cart = request.session.get('cart', [])
        return Response(
            cart,
            status=status.HTTP_200_OK
        )


    @swagger_auto_schema(
        operation_description="Remove a product from the cart.",
        responses={
            204: 'Product removed successfully.',
            404: "Product not found in the cart"
        }
    )
    def post(self, request):
        """
        Add or update a product in the cart.
        """
        serializer = CartItemSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        cart_item = serializer.validated_data
        cart = request.session.get('cart', [])

        if isinstance(cart, str):
            import json
            cart = json.loads(cart)  # Deserialize JSON string into a Python list

        if not isinstance(cart, list):
            cart = []

        t = True
        for item in cart:
            if item['product_id'] == cart_item['product_id']:
                item['quantity'] += cart_item['quantity']
                t = False
                break
        if t:
            cart.append(cart_item)

        request.session['cart'] = cart

        return Response(
            cart,
            status=status.HTTP_201_CREATED
        )



class UserCartItemView(GenericAPIView):
    permission_classes = []
    lookup_url_kwarg = 'product_id'

    def get(self, request, product_id):
        """
        get cart item by product id
        :param request:
        :param product_id:
        :return:
        """
        cart = request.session.get('cart', [])
        for cart_item in cart:
            if product_id == cart_item['product_id']:
                return Response(
                    data=cart_item,
                    status=status.HTTP_200_OK
                )

        return Response(
            data={'success': False, 'message': 'Product not found in the cart'},
            status=status.HTTP_404_NOT_FOUND
        )

    @swagger_auto_schema(
        operation_description="Remove a product from the cart.",
        responses={
            204: 'Product removed successfully.',
            404: "Product not found in the cart"
        }
    )
    def delete(self, request, product_id):
        """
        Remove a product from the cart.
        """
        cart = request.session.get('cart', [])
        for cart_item in cart:
            if product_id == cart_item['product_id']:
                cart.remove(cart_item)
                request.session['cart'] = cart
                return Response(
                    data=cart,
                    status=status.HTTP_204_NO_CONTENT
                )

        return Response(
            data={'success': False, 'message': 'Product not found in the cart'},
            status=status.HTTP_404_NOT_FOUND
        )





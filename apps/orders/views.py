from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsClient, IsCourier, IsManager
from apps.common.utils import get_nearest_courier
from apps.orders.models import OrderStatus
from apps.orders.serializers import CartItemSerializer, OrderSerializer


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
    serializer_class = CartItemSerializer
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



class OrderingView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsClient]

    def get_serializer_context(self):
        """
        Add the request object to the serializer context.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context



class NearestCourier(GenericAPIView):
    permission_classes = [IsAuthenticated, IsClient]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('latitude', openapi.IN_QUERY,
                              description="Latitude of the user's location", type=openapi.TYPE_NUMBER),
            openapi.Parameter('longitude', openapi.IN_QUERY,
                              description="Longitude of the user's location", type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: OrderSerializer(),
        },
    )
    def get(self, request, *args, **kwargs):
        client = request.user
        order = client.orders.filter(status=OrderStatus.PENDING)

        if not order.exists():
            return Response(
                data={
                    'success': False,
                    'message': "You have not any active order"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        nearest_courier, location = get_nearest_courier(latitude=latitude, longitude=longitude)

        if nearest_courier:
            order = order.first()
            order.courier = nearest_courier
            order.save()

            return Response(
                data={
                    'courier': str(nearest_courier),
                    'location': location
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'success': False,
                    'message': 'No nearest courier found'
                },
                status=status.HTTP_404_NOT_FOUND
            )




class AcceptOrderView(APIView):
    permission_classes = [IsAuthenticated, IsCourier]

    def post(self, request):
        courier = request.user

        order = courier.deliveries.filter(status=OrderStatus.PENDING).first()

        if not order:
            return Response(
                data={
                    'success': False,
                    "message": "Yoy have not any pending order.",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        order.status = OrderStatus.ACCEPTED
        order.save()

        return Response(
            data={
                'success': True,
                "message": "Order accepted successfully!",
                "order_id": order.id
            },
            status=status.HTTP_200_OK
        )



class OrderPreparationView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        manager = request.user

        order = manager.branch.orders.filter(status=OrderStatus.ACCEPTED).first()

        if not order:
            return Response(
                data={
                    'success': False,
                    "message": "Yoy have not any accepted order.",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        order.status = OrderStatus.IN_TRANSIT
        order.save()

        return Response(
            data={
                'success': True,
                "message": "Order preparation",
                "order_id": order.id
            },
            status=status.HTTP_200_OK
        )


class DeliveryOrderView(APIView):
    permission_classes = [IsAuthenticated, IsCourier]

    def post(self, request):
        courier = request.user

        order = courier.deliveries.filter(status=OrderStatus.IN_TRANSIT).first()

        if not order:
            return Response(
                data={
                    'success': False,
                    "message": "Yoy have not any order in transit.",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        order.status = OrderStatus.DELIVERED
        order.save()

        return Response(
            data={
                'success': True,
                "message": "Order delivered successfully!",
                "order_id": order.id
            },
            status=status.HTTP_200_OK
        )


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated, IsClient]

    def post(self, request):
        client = request.user

        order = client.orders.filter(status=OrderStatus.PENDING).first()

        if not order:
            return Response(
                data={
                    'success': False,
                    "message": "Yoy have not any pending order.",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        order.status = OrderStatus.CANCELLED
        order.save()

        return Response(
            data={
                'success': True,
                "message": "Order is canceled.",
                "order_id": order.id
            },
            status=status.HTTP_200_OK
        )
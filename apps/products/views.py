from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from apps.accounts.models import UserRole
from apps.accounts.permissions import IsManager
from apps.common.custom_pagination import CustomPagination
from apps.products.models import ProductModel
from apps.products.serializers import ProductSerializer
from apps.restaurants.models import BranchModel


class ProductListView(ListAPIView):
    permission_classes = [AllowAny,]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY,
                              description="Filter by category ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('restaurant_id', openapi.IN_QUERY,
                              description="Filter by restaurant ID", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: ProductSerializer(many=True),
        },
    )
    def get(self, request):
        queryset = ProductModel.objects.all()

        # Filter by category
        category_id = request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        # Filter by restaurant
        restaurant_id = request.query_params.get('restaurant_id')
        if restaurant_id:
            queryset = queryset.filter(branch__restaurant__id=restaurant_id)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductRetrieveView(RetrieveAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer
    queryset = ProductModel.objects.all()
    lookup_url_kwarg = 'pk'

class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsManager, IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.user_role == UserRole.MANAGER:
            branch = BranchModel.objects.filter(employee=user).first()
            if branch:
                return ProductModel.objects.filter(branch=branch)

        return ProductModel.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        branch = BranchModel.objects.filter(employee=user).first()
        serializer.save(branch=branch)

        return Response(
            {
                'success': True,
                'message': 'Successfully created product'
            }
        )


class ProductRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsManager]
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        user = self.request.user
        if user.user_role == UserRole.MANAGER:
            branch = BranchModel.objects.filter(employee=user).first()
            if branch:
                return ProductModel.objects.filter(branch=branch)
            else:
                return ProductModel.objects.none()
        else:
            return ProductModel.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        branch = BranchModel.objects.filter(employee=user).first()
        serializer.save(branch=branch)

    def perform_destroy(self, instance):
        user = self.request.user
        branch = BranchModel.objects.filter(employee=user).first()
        if instance.branch == branch:
            instance.delete()
        else:
            raise PermissionDenied("You can only delete products associated with your branch.")

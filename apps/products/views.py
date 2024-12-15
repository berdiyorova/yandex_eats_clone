from django.contrib.auth.models import AnonymousUser
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
from apps.common.utils import get_near_branches
from apps.products.models import ProductModel
from apps.products.serializers import ProductSerializer
from apps.restaurants.models import BranchModel


class ProductListView(ListAPIView):
    """
    Products list filter by category, restaurant, and near branches with query parameters
    """
    permission_classes = [AllowAny,]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY,
                              description="Filter by category ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('restaurant_id', openapi.IN_QUERY,
                              description="Filter by restaurant ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('latitude', openapi.IN_QUERY,
                              description="Latitude of the user's location", type=openapi.TYPE_NUMBER),
            openapi.Parameter('longitude', openapi.IN_QUERY,
                              description="Longitude of the user's location", type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: ProductSerializer(many=True),
        },
    )
    def get(self, request):
        queryset = ProductModel.objects.all()

        # Filter by near branches
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        near_branches = get_near_branches(latitude=latitude, longitude=longitude)
        if near_branches:
            branch_ids = [branch.id for branch in near_branches]
            queryset = ProductModel.objects.filter(branch__in=branch_ids)

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
    """
    Get product by pk
    """
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer
    queryset = ProductModel.objects.all()
    lookup_url_kwarg = 'pk'

class ProductListCreateAPIView(ListCreateAPIView):
    """
    Get products and create a product by branch manager
    """
    serializer_class = ProductSerializer
    permission_classes = [IsManager, IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if isinstance(user, AnonymousUser):
            return ProductModel.objects.none()

        if user.user_role == UserRole.MANAGER:
            branch = BranchModel.objects.filter(manager=user.id).first()
            if branch:
                return ProductModel.objects.filter(branch=branch)
            else:
                return ProductModel.objects.none()
        else:
            return ProductModel.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        branch = BranchModel.objects.filter(manager=user.id).first()
        product = serializer.save()
        product.branch.add(branch)

        return Response(
            {
                'success': True,
                'message': 'Successfully created product'
            }
        )


class ProductRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    RUD product by branch manager
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsManager]
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        user = self.request.user

        if isinstance(user, AnonymousUser):
            return ProductModel.objects.none()

        if user.user_role == UserRole.MANAGER:
            branch = BranchModel.objects.filter(manager=user).first()
            if branch:
                return ProductModel.objects.filter(branch=branch)
            else:
                return ProductModel.objects.none()
        else:
            return ProductModel.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        branch = BranchModel.objects.filter(manager=user).first()
        serializer.save(branch=branch)

    def perform_destroy(self, instance):
        user = self.request.user
        branch = BranchModel.objects.filter(manager=user).first()
        if instance.branch == branch:
            instance.delete()
        else:
            raise PermissionDenied("You can only delete products associated with your branch.")

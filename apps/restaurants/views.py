from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.accounts.models import UserModel, UserRole
from apps.accounts.permissions import IsOwner
from apps.common.custom_pagination import CustomPagination
from apps.common.utils import create_user
from apps.restaurants.models import BranchModel, RestaurantModel
from apps.restaurants.serializers import BranchSerializer, ManagerSerializer, RestaurantSerializer, \
    OwnerDeliverySerializer


class RestaurantViewSet(ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = RestaurantModel.objects.all()
    pagination_class = CustomPagination


class OwnerViewSet(ModelViewSet):
    serializer_class = OwnerDeliverySerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['post', 'get', 'delete']
    pagination_class = CustomPagination

    def get_queryset(self):
        return UserModel.objects.filter(user_role=UserRole.OWNER)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = create_user(serializer, UserRole.OWNER)
        return Response(data=validated_data, status=status.HTTP_201_CREATED)



class DeliveryViewSet(ModelViewSet):
    serializer_class = OwnerDeliverySerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['post', 'get', 'delete']
    pagination_class = CustomPagination

    def get_queryset(self):
        return UserModel.objects.filter(user_role=UserRole.DELIVERY)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = create_user(serializer, UserRole.DELIVERY)
        return Response(data=validated_data, status=status.HTTP_201_CREATED)


class BranchViewSet(ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [IsOwner, IsAuthenticated]
    queryset = BranchModel.objects.all()
    pagination_class = CustomPagination


class EmployeeViewSet(ModelViewSet):
    serializer_class = ManagerSerializer
    permission_classes = [IsOwner, IsAuthenticated]
    queryset = UserModel.objects.all()
    http_method_names = ['get', 'post', 'delete']


    def get_queryset(self):
        return UserModel.objects.filter(user_role=UserRole.MANAGER)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = create_user(serializer=serializer, user_role=UserRole.MANAGER)
        return Response(data=validated_data, status=status.HTTP_201_CREATED)

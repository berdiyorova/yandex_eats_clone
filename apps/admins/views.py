from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.accounts.models import UserModel, UserRole, AuthStatus
from apps.common.utils import create_user
from apps.restaurants.models import RestaurantModel
from apps.admins.serializers import RestaurantSerializer, ManagerDeliverySerializer


class RestaurantViewSet(ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = RestaurantModel.objects.all()


class ManagerViewSet(ModelViewSet):
    serializer_class = ManagerDeliverySerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['post', 'get', 'delete']

    def get_queryset(self):
        return UserModel.objects.filter(user_role=UserRole.MANAGER)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = create_user(serializer, UserRole.MANAGER)
        return Response(data=validated_data, status=status.HTTP_201_CREATED)



class DeliveryViewSet(ModelViewSet):
    serializer_class = ManagerDeliverySerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['post', 'get', 'delete']

    def get_queryset(self):
        return UserModel.objects.filter(user_role=UserRole.DELIVERY)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = create_user(serializer, UserRole.DELIVERY)
        return Response(data=validated_data, status=status.HTTP_201_CREATED)

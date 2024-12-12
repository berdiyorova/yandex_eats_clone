from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.accounts.models import UserModel, UserRole
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



class DeliveryViewSet(ModelViewSet):
    serializer_class = ManagerDeliverySerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['post', 'get', 'delete']

    def get_queryset(self):
        return UserModel.objects.filter(user_role=UserRole.DELIVERY)

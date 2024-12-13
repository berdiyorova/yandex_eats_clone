from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import UserModel, UserRole
from apps.accounts.permissions import IsManager
from apps.common.utils import create_user
from apps.restaurants.models import BranchModel
from apps.manager.serializers import BranchSerializer, EmployeeSerializer


class BranchViewSet(ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [IsManager, IsAuthenticated]
    queryset = BranchModel.objects.all()


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsManager, IsAuthenticated]
    queryset = UserModel.objects.all()
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return UserModel.objects.filter(user_role=UserRole.EMPLOYEE)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = create_user(serializer=serializer, user_role=UserRole.EMPLOYEE)
        return Response(data=validated_data, status=status.HTTP_201_CREATED)

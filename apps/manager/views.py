from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsManager
from apps.restaurants.models import BranchModel
from apps.manager.serializers import BranchSerializer



class BranchViewSet(ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [IsManager, IsAuthenticated]
    queryset = BranchModel.objects.all()

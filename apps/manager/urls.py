from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.manager import views

router = DefaultRouter()
router.register(prefix=r'branches/', viewset=views.BranchViewSet, basename='branches')

urlpatterns = [
    path('', include(router.urls)),
]
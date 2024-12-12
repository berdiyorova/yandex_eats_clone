from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.admins import views

router = DefaultRouter()
router.register(prefix=r'restaurants', viewset=views.RestaurantViewSet, basename='restaurants')
router.register(prefix=r'manager', viewset=views.ManagerViewSet, basename='manager')
router.register(prefix=r'delivery', viewset=views.DeliveryViewSet, basename='delivery')

urlpatterns = [
    path('', include(router.urls)),
]
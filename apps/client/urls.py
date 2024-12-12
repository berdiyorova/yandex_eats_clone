from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.client import views

router = DefaultRouter()
router.register(prefix=r'my-addresses/', viewset=views.ClientAddressViewSet, basename='my-addresses')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginViaPhoneView.as_view()),
    path('verify/', views.VerifyView.as_view()),
    path('verify/resend/', views.ResendVerifyView.as_view()),
] + router.urls

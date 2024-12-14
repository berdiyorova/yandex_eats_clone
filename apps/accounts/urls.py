from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.accounts import views

router = DefaultRouter()
router.register(prefix=r'client/addresses', viewset=views.ClientAddressViewSet, basename='my-addresses')

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('client/register/', views.RegisterView.as_view(), name='register'),
    path('login_via_phone/', views.LoginViaPhoneView.as_view()),
    path('verify/', views.VerifyView.as_view()),
    path('verify/resend/', views.ResendVerifyView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('forgot-password/', views.ForgotPasswordView.as_view()),
    path('reset-password/', views.ResetPasswordView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),
] + router.urls

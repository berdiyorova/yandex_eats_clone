from django.urls import path

from apps.client import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginViaPhoneView.as_view()),
    path('verify/', views.VerifyView.as_view()),
    # path('verify/resend/', views.ResendVerifyView.as_view()),
]

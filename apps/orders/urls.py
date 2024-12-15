from django.urls import path

from apps.orders import views

urlpatterns = [
    path('cart/items/', views.UserCartView.as_view()),
    path('cart/item/<int:product_id>/', views.UserCartItemView.as_view()),
]

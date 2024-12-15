from django.urls import path

from apps.orders import views

urlpatterns = [
    path('client/cart/items/', views.UserCartView.as_view()),
    path('client/cart/item/<int:product_id>/', views.UserCartItemView.as_view()),
    path('client/ordering/', views.OrderingView.as_view()),
    path('client/nearest_courier/', views.NearestCourier.as_view()),
    path('client/cancel_order/', views.CancelOrderView.as_view()),

    path('courier/accept_order/', views.AcceptOrderView.as_view()),
    path('manager/preparation_order/', views.OrderPreparationView.as_view()),
    path('manager/delivery_order/', views.DeliveryOrderView.as_view()),
]

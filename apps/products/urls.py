from django.urls import path

from apps.products import views


urlpatterns = [
    path('', views.ProductListView.as_view()),
    path('<int:pk>/', views.ProductRetrieveView.as_view()),
    path('branch_manager/list/create/', views.ProductListCreateAPIView.as_view()),
    path('branch_manager/ret/up/del/<int:pk>/', views.ProductRetrieveUpdateDeleteView.as_view()),
]

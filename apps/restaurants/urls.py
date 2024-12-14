from rest_framework.routers import DefaultRouter

from apps.restaurants import views

router = DefaultRouter()
router.register(prefix=r'admin', viewset=views.RestaurantViewSet, basename='restaurants')
router.register(prefix=r'admin/owner', viewset=views.OwnerViewSet, basename='manager')
router.register(prefix=r'admin/delivery', viewset=views.DeliveryViewSet, basename='delivery')

router.register(prefix=r'owner/branches', viewset=views.BranchViewSet, basename='branches')
router.register(prefix=r'owner/managers', viewset=views.EmployeeViewSet, basename='employees')

urlpatterns = [

] + router.urls

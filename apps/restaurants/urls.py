from rest_framework.routers import DefaultRouter

from apps.restaurants import views

router = DefaultRouter()
router.register(prefix=r'admin', viewset=views.RestaurantViewSet, basename='restaurants')
router.register(prefix=r'admin/owner', viewset=views.OwnerViewSet, basename='owner')
router.register(prefix=r'admin/courier', viewset=views.CourierViewSet, basename='courier')

router.register(prefix=r'owner/branches', viewset=views.BranchViewSet, basename='branches')
router.register(prefix=r'owner/managers', viewset=views.ManagerViewSet, basename='managers')

urlpatterns = [

] + router.urls

from django.contrib import admin
from apps.restaurants.models import RestaurantModel, BranchModel

@admin.register(RestaurantModel)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('id', 'name',)
    list_filter = ('created_at',)


@admin.register(BranchModel)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'get_restaurant_name')
    search_fields = ('id', 'restaurant__name',)
    list_filter = ('restaurant__name', 'created_at')

    def get_restaurant_name(self, obj):
        return obj.restaurant.name

    get_restaurant_name.short_description = 'Restaurant Name'

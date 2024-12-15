from rest_framework import serializers

from apps.products.models import ProductModel, CategoryModel
from apps.restaurants.models import BranchModel


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all(), many=True)
    branch = serializers.PrimaryKeyRelatedField(queryset=BranchModel.objects.all())
    restaurant = serializers.SerializerMethodField('get_restaurant')

    class Meta:
        model = ProductModel
        fields = '__all__'
        read_only_fields = ('real_price',)

    def get_restaurant(self, obj):
        return obj.branch.restaurant.name


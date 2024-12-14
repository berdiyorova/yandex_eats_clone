from rest_framework import serializers

from apps.products.models import ProductModel, CategoryModel


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all(), many=True)
    branch = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    restaurant = serializers.SerializerMethodField('get_restaurant')

    class Meta:
        model = ProductModel
        fields = '__all__'

    def get_restaurant(self, obj):
        return obj.branch.first().restaurant.name


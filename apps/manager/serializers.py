from decimal import Decimal

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.common.utils import get_full_address
from apps.restaurants.models import RestaurantModel, BranchModel


class BranchSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=RestaurantModel.objects.all())

    class Meta:
        model = BranchModel
        fields = ('id', 'restaurant', 'address', 'longitude', 'latitude')
        read_only_fields = ('address',)
        validators = [
            UniqueTogetherValidator(
                queryset=BranchModel.objects.all(),
                fields=['longitude', 'latitude'],
                message="There is already a branch at this location"
            )
        ]


    def create(self, validated_data):
        longitude = validated_data.get('longitude')
        latitude = validated_data.get('latitude')

        validated_data['address'] = get_full_address(longitude=Decimal(longitude), latitude=Decimal(latitude))

        branch = BranchModel.objects.create(**validated_data)
        return branch

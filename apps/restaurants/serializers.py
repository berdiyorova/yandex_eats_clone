from decimal import Decimal

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from apps.accounts.models import UserModel, UserRole
from apps.common.utils import get_full_address, check_password
from apps.restaurants.models import RestaurantModel, BranchModel



class RestaurantSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.filter(user_role=UserRole.OWNER))

    class Meta:
        model = RestaurantModel
        fields = ('id', 'name', 'address', 'longitude', 'latitude', 'manager', )
        read_only_fields = ('address',)
        validators = [
            UniqueTogetherValidator(
                queryset=RestaurantModel.objects.all(),
                fields=['longitude', 'latitude'],
                message="There is already a restaurant at this location"
            )
        ]

    def create(self, validated_data):
        longitude = validated_data.get('longitude')
        latitude = validated_data.get('latitude')

        validated_data['address'] = get_full_address(longitude=Decimal(longitude), latitude=Decimal(latitude))

        branch = RestaurantModel.objects.create(**validated_data)
        return branch




class OwnerManageCourierSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    username = serializers.CharField(validators=[UniqueValidator(
        queryset=UserModel.objects.all(),
        message="This username is already registered")
    ])

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'user_role', 'auth_status', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'user_role': {'read_only': True},
            'auth_status': {'read_only': True},
        }

    def validate(self, attrs):
        return check_password(attrs)




class BranchSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=RestaurantModel.objects.all())

    class Meta:
        model = BranchModel
        fields = ('id', 'restaurant', 'name', 'address', 'longitude', 'latitude')
        read_only_fields = ('address', 'name')
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
        restaurant = validated_data['restaurant']
        validated_data['name'] = restaurant.name

        branch = BranchModel.objects.create(**validated_data)
        return branch

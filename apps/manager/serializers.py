import re
from decimal import Decimal

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from apps.accounts.models import UserModel, UserRole
from apps.common.utils import get_full_address, check_password
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



class EmployeeSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    username = serializers.CharField(validators=[UniqueValidator(
        queryset=UserModel.objects.all(),
        message="This username is already registered")
    ])

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'user_role', 'auth_status', 'password',
                  'confirm_password')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'user_role': {'read_only': True},
            'auth_status': {'read_only': True},
        }

    def validate(self, attrs):
        return check_password(attrs)

    def validate_user_role(self, value):
        if value != UserRole.EMPLOYEE:
            raise serializers.ValidationError("User role must be only EMPLOYEE.")

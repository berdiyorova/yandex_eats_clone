import re
from decimal import Decimal

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from apps.accounts.models import UserModel, UserRole
from apps.common.utils import get_full_address
from apps.restaurants.models import RestaurantModel


class RestaurantSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.filter(user_role=UserRole.MANAGER))

    class Meta:
        model = RestaurantModel
        fields = ('id', 'name', 'address', 'longitude', 'latitude', 'manager')
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




class ManagerDeliverySerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    phone_number = serializers.CharField(validators=[UniqueValidator(
        queryset=UserModel.objects.all(),
        message="This phone number is already registered")
    ])
    username = serializers.EmailField(validators=[UniqueValidator(
        queryset=UserModel.objects.all(),
        message="This username is already registered")
    ])

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'phone_number', 'username', 'user_role', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }


    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        if password:
            try:
                validate_password(password=password)
            except Exception as e:
                raise serializers.ValidationError(str(e))

        return attrs

    def validate_phone_number(self, value):
        """ Raise a ValidationError if the value looks like a mobile telephone number.
        """
        pattern = re.compile(
            r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))")

        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid mobile number format.")
        return value


    def validate_user_role(self, value):
        if value not in [UserRole.MANAGER, UserRole.DELIVERY]:
            raise serializers.ValidationError("User role must be only MANAGER or DELIVERY.")

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        if not validated_data.get('user_role'):
            validated_data['user_role'] = UserRole.DELIVERY

        user = UserModel.objects.create(
            **validated_data
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user


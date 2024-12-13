import re

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import UserModel
from apps.common.utils import check_phone_number, check_password


class VerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)


class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = UserModel.objects.get(username=username)
        authenticated_user = authenticate(username=user.username, password=password)

        if not authenticated_user:
            raise serializers.ValidationError("Username or password is not valid")

        return user.token()


class ChangeUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'phone_number']

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['success'] = True
        representation['message'] = 'User updated successfully'
        return representation



class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number', None)
        phone = check_phone_number(phone_number)

        user = UserModel.objects.filter(phone_number=phone)
        if not user.exists():
            raise NotFound(detail="User not found")
        attrs['user'] = user.first()
        return attrs
    
    
class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = (
            'password',
            'confirm_password'
        )

    def validate(self, attrs):
        return check_password(attrs)

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        return super(ResetPasswordSerializer, self).update(instance, validated_data)



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        return check_password(attrs)

    def update(self, instance, validated_data):
        old_password = validated_data.pop('old_password')
        if not instance.check_password(old_password):
            raise serializers.ValidationError("Invalid old password")

        new_password = validated_data.pop('password')
        instance.set_password(new_password)
        return super(ChangePasswordSerializer, self).update(instance, validated_data)



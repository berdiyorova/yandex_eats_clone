import re

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import UserModel



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
        fields = ['first_name', 'last_name', 'username']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False},
        }

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
        pattern = re.compile(
            r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))")

        if not re.match(pattern, phone_number):
            raise serializers.ValidationError("Invalid mobile number format.")

        user = UserModel.objects.filter(phone_number=phone_number)
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
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)
        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    'success': False,
                    'message': "Passwords do not match."
                }
            )
        if password:
            try:
                validate_password(password=password)
            except Exception as e:
                raise serializers.ValidationError(str(e))
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        return super(ResetPasswordSerializer, self).update(instance, validated_data)



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password', None)
        confirm_password = attrs.get('confirm_password', None)

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    'success': False,
                    'message': "Passwords do not match."
                }
            )
        if new_password:
            try:
                validate_password(password=new_password)
            except Exception as e:
                raise serializers.ValidationError(str(e))
        return attrs

    def update(self, instance, validated_data):
        old_password = validated_data.pop('old_password')
        if not instance.check_password(old_password):
            raise serializers.ValidationError("Invalid old password")

        new_password = validated_data.pop('new_password')
        instance.set_password(new_password)
        return super(ChangePasswordSerializer, self).update(instance, validated_data)



import re

from rest_framework import serializers

from apps.accounts.models import UserModel, UserRole
from apps.client.models import ClientAddress


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'phone_number',)

    def validate(self, attrs):
        phone = attrs.get('phone_number')
        pattern = re.compile(
            r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))")

        if not re.match(pattern, phone):
            raise serializers.ValidationError("Invalid mobile number format.")

        user = UserModel.objects.filter(phone_number=phone).first()
        if user:
            raise serializers.ValidationError("Phone number already registered")

        return attrs


    def to_representation(self, instance):
        data = super(RegisterSerializer, self).to_representation(instance)
        data.update({'user_role': instance.user_role})
        data.update(instance.token())
        return data



class LoginViaPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True)


    def validate(self, attrs):
        phone = attrs.get('phone_number')
        pattern = re.compile(
            r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))")

        if not re.match(pattern, phone):
            raise serializers.ValidationError("Invalid mobile number format.")

        return attrs


class VerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)



class ClientAddressSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(
        read_only=True,
        queryset=UserModel.objects.filter(user_role=UserRole.CLIENT)
    )

    class Meta:
        model = ClientAddress
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
            'home_number': {'required': False},
            'door_phone': {'required': False},
            'entrance': {'required': False},
            'floor': {'required': False},
            'instructions': {'required': False},
        }

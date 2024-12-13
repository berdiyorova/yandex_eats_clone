import re

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from geopy.geocoders import Nominatim
from twilio.rest import Client
from rest_framework.serializers import ValidationError

from apps.accounts.models import AuthStatus, UserModel


def get_full_address(longitude, latitude):
    """This is open source map api to get full address, if it does not work return False"""
    try:
        geolocator = Nominatim(user_agent="yandex_eats")
        location = geolocator.reverse(f"{longitude}, {latitude}")
        return location.address
    except Exception:
        raise Exception("Sorry, something went wrong.")


def send_verify_code_to_phone(phone, code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=f"Your instagram verification code is: {code}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )

def check_password(attrs):
    password = attrs.get('password')
    confirm_password = attrs.get('confirm_password')

    if password != confirm_password:
        raise ValidationError("Passwords do not match")

    if password:
        try:
            validate_password(password=password)
        except Exception as e:
            raise ValidationError(str(e))

    return attrs


def check_phone_number(value):
    """ Raise a ValidationError if the value looks like a mobile telephone number.
    """
    pattern = re.compile(
        r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))")

    if not re.match(pattern, value):
        raise ValidationError("Invalid mobile number format.")
    return value


def create_user(serializer, user_role):
    validated_data = serializer.validated_data.copy()
    validated_data.pop('confirm_password', None)

    validated_data['user_role'] = user_role
    validated_data['auth_status'] = AuthStatus.DONE

    user = UserModel(**validated_data)
    user.set_password(validated_data.pop('password'))
    user.save()

    return validated_data

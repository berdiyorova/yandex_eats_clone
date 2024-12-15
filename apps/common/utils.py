import re

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from twilio.rest import Client
from rest_framework.serializers import ValidationError

from apps.accounts.models import AuthStatus, UserModel
from apps.common.constants import BRANCH_SEARCH_RADIUS
from apps.restaurants.models import BranchModel


def get_full_address(longitude, latitude):
    """
    This is open source map api to get full address
    """
    try:
        geolocator = Nominatim(user_agent="yandex_eats")
        location = geolocator.reverse(f"{longitude}, {latitude}")
        return location.address
    except Exception:
        raise Exception("Sorry, something went wrong.")


def send_verify_code_to_phone(phone, code):
    """
    Send a verification code by SMS to user phone number
    :param phone:
    :param code:
    :return:
    """
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=f"Your instagram verification code is: {code}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )

def check_password(attrs):
    """
    Raise a ValidationError if the passwords do not match or invalid
    :param attrs:
    :return:
    """
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
    """
    Raise a ValidationError if the value looks like a mobile telephone number.
    """
    pattern = re.compile(
        r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))")

    if not re.match(pattern, value):
        raise ValidationError("Invalid mobile number format.")

    return value


def create_user(serializer, user_role):
    """
    CRUD owner or delivery by admin,  or manager by owner
    :param serializer:
    :param user_role:
    :return:
    """
    validated_data = serializer.validated_data.copy()
    validated_data.pop('confirm_password', None)

    validated_data['user_role'] = user_role
    validated_data['auth_status'] = AuthStatus.DONE

    user = UserModel(**validated_data)
    user.set_password(validated_data.pop('password'))
    user.save()

    return validated_data




def get_near_branches(latitude, longitude):
    if latitude and longitude:
        user_location = (float(latitude), float(longitude))
        near_branches = {}

        for branch in BranchModel.objects.all():
            branch_location = (branch.latitude, branch.longitude)
            distance = geodesic(user_location, branch_location).kilometers

            if distance <= BRANCH_SEARCH_RADIUS:
                if branch.name not in near_branches or near_branches[branch.name].product_set.count() < branch.product_set.count():
                    near_branches[branch.name] = branch

        return list(near_branches.values())
    else:
        return []

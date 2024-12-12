from django.conf import settings
from geopy.geocoders import Nominatim
from twilio.rest import Client


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

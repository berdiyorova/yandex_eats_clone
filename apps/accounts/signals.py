from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client

from Config import settings
from apps.accounts.models import UserModel


@receiver(post_save, sender=UserModel)
def send_verify_code_to_user(sender, instance, created, **kwargs):
    if instance.phone_number:
        if created:
            code = instance.create_verify_code()

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            client.messages.create(
                body=f"Your Yandex_Eats verification code is: {code}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=instance.phone_number
            )

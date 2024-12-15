import random
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models, IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel, AddressModel


class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'ADMIN'
    OWNER = 'OWNER', 'OWNER'
    MANAGER = 'MANAGER', 'MANAGER'
    COURIER = 'COURIER', 'COURIER'
    CLIENT = 'CLIENT', 'CLIENT'



class AuthStatus(models.TextChoices):
    NEW = 'NEW', 'NEW'
    DONE = 'DONE', 'DONE'



class UserModel(AbstractUser, BaseModel):
    id = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    user_role = models.CharField(max_length=50, choices=UserRole.choices, default=UserRole.CLIENT)
    auth_status = models.CharField(max_length=50, choices=AuthStatus.choices, default=AuthStatus.NEW)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return self.get_full_name()


    def __str__(self):
        return self.full_name


    def create_verify_code(self):
        code = ''.join(random.choices('0123456789', k=4))

        UserConfirmModel.objects.create(
            code=code,
            user=self,
        )
        return code


    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }


    def check_username(self):
        if not self.username:
            temp_username = f"yandex-{uuid.uuid4().__str__().split('-')[-1]}"
            while UserModel.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(0, 9)}"
            self.username = temp_username


    def check_pass(self):
        if not self.password:
            temp_password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"
            self.set_password(temp_password)


    def save(self, *args, **kwargs):
        self.check_username()
        self.check_pass()
        super(UserModel, self).save(*args, **kwargs)



class UserConfirmModel(BaseModel):
    code = models.CharField(max_length=4)
    is_confirmed = models.BooleanField(default=False)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='verify_codes')

    def __str__(self):
        return f"{self.user.__str__()} - {self.code}"

    class Meta:
        verbose_name = 'Verification code'
        verbose_name_plural = 'Verification codes'
        unique_together = ('user', 'code')



class ClientAddress(AddressModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    home_number = models.CharField(max_length=10, null=True, blank=True)
    door_phone = models.CharField(max_length=20, null=True, blank=True)
    entrance = models.PositiveSmallIntegerField(null=True, blank=True)
    floor = models.PositiveSmallIntegerField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)

    client = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="addresses")

    class Meta:
        verbose_name = 'Client Address'
        verbose_name_plural = 'Client Addresses'
        unique_together = ('address', 'client')



class CourierAddress(AddressModel):
    courier = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="locations")

    class Meta:
        verbose_name = 'Courier Address'
        verbose_name_plural = 'Courier Addresses'
        unique_together = ('address', 'courier')

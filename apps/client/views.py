from datetime import timedelta

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.base.exceptions import TwilioRestException

from Config.settings import VERIFY_CODE_EXPIRE_TIME
from apps.accounts.models import UserModel
from apps.client.serializers import RegisterSerializer, LoginViaPhoneSerializer, VerifySerializer
from apps.common.utils import send_verify_code_to_phone


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny,]



class LoginViaPhoneView(GenericAPIView):
    permission_classes = [AllowAny,]
    queryset = UserModel.objects.all()
    serializer_class = LoginViaPhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get('phone_number')
        try:
            user = UserModel.objects.filter(phone_number=phone).first()
        except UserModel.DoesNotExists:
            raise ValidationError("You have not registered")

        code = user.create_verify_code()
        send_verify_code_to_phone(user.phone_number, code)
        response = user.token()
        response['success'] = True
        response['message'] = 'We have sent you a verification code.'

        return Response(data=response, status=status.HTTP_200_OK)


class VerifyView(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = UserModel.objects.all()
    serializer_class = VerifySerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        code = serializer.validated_data.get('code')

        self.check_verify(user, code)

        return Response(
            data={
                'success': True,
                'access': user.token()['access_token'],
                'refresh': user.token()['refresh_token']
            }
        )

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(
            created_at__gte=timezone.now() - VERIFY_CODE_EXPIRE_TIME,
            code=code,
            is_confirmed=False)

        if not verifies.exists():
            data = {
                'success': False,
                'message': 'Your verification code is incorrect or out of date.'
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)

        return True


class ResendVerifyView(APIView):
    permission_classes = [IsAuthenticated, ]
    queryset = UserModel.objects.all()

    def get(self, *args, **kwargs):
        user = self.request.user

        self.check_verification(user=user)
        try:
            code = user.create_verify_code()
            send_verify_code_to_phone(user.phone_number, code)
        except TwilioRestException as e:
            data = {
                'success': False,
                'message': 'Failed to send verification code. Please try again later.'
            }
            raise ValidationError(data)

        return Response(
            data={
                'success': True,
                'message': 'Your verification code has been resent.'
            }, status=status.HTTP_200_OK
        )

    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(
            created_at__gte=timezone.now() - VERIFY_CODE_EXPIRE_TIME,
            is_confirmed=False)

        if verifies.exists():
            data = {
                "message": "Your code is still usable. Wait a moment."
            }
            raise ValidationError(data)


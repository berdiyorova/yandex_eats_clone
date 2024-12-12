from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.models import UserModel
from apps.accounts.serializers import LoginSerializer, ChangeUserInfoSerializer, ForgotPasswordSerializer, \
    ResetPasswordSerializer, ChangePasswordSerializer
from apps.common.utils import send_verify_code_to_phone


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer



class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema()
    def post(self, request, *args, **kwargs):
        try:
            refresh = self.request.data.get('refresh')
            token = RefreshToken(refresh)
            token.blacklist()
        except TokenError as e:
            raise ValidationError(str(e))
        return Response({
            'success': True,
            'message': 'You are logged out'
        }, status=status.HTTP_205_RESET_CONTENT)


class ChangeUserInformationView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeUserInfoSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user


class ForgotPasswordView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        user = serializer.validated_data.get('user')

        code = user.create_verify_code()
        send_verify_code_to_phone(phone_number, code)

        return Response(
            {
                "success": True,
                'message': "Verification code successfully submitted",
                "access": user.token()['access_token'],
                "refresh": user.token()['refresh_token'],
            }, status=status.HTTP_200_OK
        )


class ResetPasswordView(UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        return Response(
            {
                'success': True,
                'message': "Your password has been reset",
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token'],
            }
        )



class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer
    queryset = UserModel.objects.all()
    http_method_names = ['patch',]

    def get_object(self):
        return self.request.user

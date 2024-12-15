from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, UpdateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.models import UserModel, AuthStatus, ClientAddress
from apps.accounts.permissions import IsClient
from apps.accounts.serializers import LoginSerializer, ForgotPasswordSerializer, \
    ResetPasswordSerializer, ChangePasswordSerializer, VerifySerializer, LoginViaPhoneSerializer, \
    ClientAddressSerializer, RegisterSerializer, UserSerializer
from apps.common.constants import VERIFY_CODE_EXPIRE_TIME
from apps.common.utils import send_verify_code_to_phone




class RegisterView(CreateAPIView):
    """
    Register view for client users
   """
    serializer_class = RegisterSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny,]


class VerifyView(GenericAPIView):
    """
   Verify the phone number using the verification code
   """
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
            if user.auth_status == AuthStatus.NEW:
                user.auth_status = AuthStatus.DONE
                user.save()

        return True


class ResendVerifyView(APIView):
    """
   A verification code will be sent again
   """
    permission_classes = [IsAuthenticated, ]
    queryset = UserModel.objects.all()

    def get(self, *args, **kwargs):
        user = self.request.user

        self.check_verification(user=user)

        code = user.create_verify_code()
        send_verify_code_to_phone(user.phone_number, code)

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


class LoginView(TokenObtainPairView):
    """
    Log in with basic authentication
    """
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


class ProfileView(RetrieveUpdateDestroyAPIView):
    """
    Get user profile info and edit it
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def get_object(self):
        return self.request.user


class ForgotPasswordView(GenericAPIView):
    """
    User identification by phone number when the password is forgotten
    """
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
    """
    Reset a forgotten password
    """
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
    """
    Change old password to new password
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer
    queryset = UserModel.objects.all()
    http_method_names = ['patch',]

    def get_object(self):
        return self.request.user


class LoginViaPhoneView(GenericAPIView):
    """
    For client users, log in with phone number
    """
    permission_classes = [IsClient,]
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



class ClientAddressViewSet(ModelViewSet):
    """
    CRUD for client addresses
    """
    permission_classes = [IsClient, IsAuthenticated]
    serializer_class = ClientAddressSerializer
    queryset = ClientAddress.objects.all()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        return ClientAddress.objects.filter(client=self.request.user)

    def create(self, request, *args, **kwargs):
        client = self.request.user
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(client=client)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

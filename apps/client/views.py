from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.models import UserModel
from apps.client.models import ClientAddress
from apps.client.serializers import RegisterSerializer, LoginViaPhoneSerializer, \
    ClientAddressSerializer
from apps.accounts.permissions import IsClient
from apps.common.utils import send_verify_code_to_phone


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny,]



class LoginViaPhoneView(GenericAPIView):
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
    permission_classes = [IsAuthenticated, IsClient]
    serializer_class = ClientAddressSerializer
    queryset = ClientAddress.objects.all()

    def get_queryset(self):
        return ClientAddress.objects.filter(client=self.request.user)

    def create(self, request, *args, **kwargs):
        client = self.request.user
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        address = ClientAddress.objects.create(
            client=client,
            **serializer.validated_data
        )
        return address

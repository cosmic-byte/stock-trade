from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView)
from rest_framework_jwt.serializers import (
    jwt_payload_handler,
    jwt_encode_handler
)

from stock_trade.apps.user.models import AppAdmin
from stock_trade.apps.user.serializer import (
    UserCreateSerializer,
    EnableDisableUserSerializer,
    DeleteUserSerializer,
    CreateAdminSerializer,
    RetrieveAdminSerializer
)
from stock_trade.permissions import CustomDjangoModelPermissions
from stock_trade.utils.model_utils import get_object_or_400

User = get_user_model()


class UserCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.data)
        payload = jwt_payload_handler(user)
        response = {
            'token': jwt_encode_handler(payload),
            'user': serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)


class EnableOrDisableUser(UpdateAPIView):
    permission_classes = (CustomDjangoModelPermissions,)
    queryset = User.objects.all()
    serializer_class = EnableDisableUserSerializer
    lookup_field = 'uid'


class DeleteUserView(UpdateAPIView):
    permission_classes = (CustomDjangoModelPermissions,)
    queryset = User.objects.all()
    serializer_class = DeleteUserSerializer
    lookup_field = 'uid'


class ActivateAccountView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        uid = force_text(urlsafe_base64_decode(self.kwargs.get('uidb64')))
        token = self.kwargs.get('token')
        user = User.objects.get_object_or_404(uid=uid)
        # if user and account_activation_token.check_token(user, token):
        #     user.email_verified = True
        #     user.save()
        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data)


class AdminViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = AppAdmin.objects.all()
    serializer_class = CreateAdminSerializer
    permission_classes = (CustomDjangoModelPermissions,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_400(queryset, user=self.request.user)
        return obj

    def retrieve(self, request, *args, **kwargs):
        serializer = RetrieveAdminSerializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

import logging
import secrets

from django.contrib.auth.hashers import make_password
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from app import models
from app import serializers
from authentication.models import AccessKey
from authentication.permissions import IsAppUser, WithBootstrapToken
from src.base.viewset import ModelViewSet

logger = logging.getLogger(__name__)


class RegistrationViewSet(ModelViewSet):
    permission_classes_mapping = {
        'list': (permissions.AllowAny,),
        'create': (permissions.AllowAny,),
        'telegram': (IsAppUser,),
        'terminal': (WithBootstrapToken,)
    }

    def perform_authentication(self, request):
        """
        Perform authentication on the incoming request.

        Note that if you override this and simply 'pass', then authentication
        will instead be performed lazily, the first time either
        `request.user` or `request.auth` is accessed.
        """
        request.user

    # @permission_classes((permissions.AllowAny, ))
    def list(self, request, *args, **kwargs):
        serializer_class = serializers.UserListSerializer
        queryset = models.UserProfile.objects.all()
        # print(request.GET)
        name = request.GET.get('name')

        return Response(serializer_class(queryset.filter(username=name).all(), many=True).data)

    # @permission_classes([permissions.AllowAny, ])
    def create(self, request, *args, **kwargs):
        serializer_class = serializers.UserSerializer
        data = request.data
        data['name'] = data.get('username')
        data['password'] = make_password(data.get('password'))
        data['role'] = 'user'

        serializer = serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            # token, created = Token.objects.get_or_create(user=user)
            # self.send_auth_signal(success=True, user=user)

            return Response({
                'token': token.key,
                'username': user.username,
                # 'user_id': user.pk,
                # 'email': user.email
            })
            # return Response(serializer_class(instance=user).data)

        else:
            return Response(serializer.errors)

    # @permission_classes([IsAppUser, ])
    @action(methods=['post'], detail=False, url_path='telegram-registrations')
    def telegram(self, request, *args, **kwargs):
        tgid = request.data.get("tgid")
        token = request.data.get("token")

        telegram_obj = models.Telegram.objects.filter(token=token)
        if telegram_obj:
            telegram_obj = telegram_obj.first()
            if telegram_obj.status:
                return Response({"message": "已綁定過了，重新綁定需先解除再綁一次"})
            telegram_obj.chat_id = tgid
            telegram_obj.status = True
            telegram_obj.save()
            return Response({"message": "綁定成功"})
        else:
            return Response({"message": "綁定失敗，Token錯誤"})

    # @permission_classes([WithBootstrapToken])
    @action(methods=['post'], detail=False, url_path='terminal-registrations')
    def terminal(self, request, *args, **kwargs):
        User = models.UserProfile

        username = request.data.get('name')
        comment = request.data.get('comment')

        if User.objects.filter(username=username):
            return Response({"code": '名稱重複'}, status=401)
        user = User.objects.create_user(username=username, password=secrets.token_urlsafe(8))
        user.name = username
        user.role = 'App'
        user.is_staff = True
        user.save()
        AccessKey.objects.create(user=user)
        data = {k: v for k, v in request.data.items()}
        sa_serializer = serializers.ServiceAccountSerializer(instance=user)
        data['service_account'] = sa_serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

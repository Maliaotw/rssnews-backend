import logging
import uuid

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from app import models
from app import serializers
from authentication.permissions import IsAppUser, IsValidUser
from src.base.viewset import ModelViewSet

logger = logging.getLogger(__name__)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            # token, created = Token.objects.get_or_create(user=user)
            # self.send_auth_signal(success=True, user=user)

            return Response({
                'token': token,
                'user': user.username,
                # 'user_id': user.pk,
                # 'email': user.email
            })
        else:
            logging.debug('UserLoginView form_invalid')
            raise ValidationError(serializer.errors)


class UserProfileViewSet(ModelViewSet):
    _User = get_user_model()
    model_class = _User  # User
    queryset = model_class.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsValidUser | IsAppUser,)

    serializer_action_classes = {
        'list': serializers.UserprofileSerializer,
        'create': serializers.UserprofileSerializer,
        'update': serializers.UserprofileSerializer,
        'retrieve': serializers.UserprofileSerializer
    }

    def list(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

    @action(methods=['post'], detail=False)
    def source(self, request, *args, **kwargs):
        checkedKeys = request.data.get('checkedKeys')
        checkedKeys_list = list(filter(lambda x: isinstance(x, int), checkedKeys))
        # request.user.sourse.clear()
        request.user.sourse.set(list(models.Source.objects.filter(id__in=checkedKeys_list)))
        # print(request.user.sourse.all())
        return Response({'message': "ok"})

    @action(methods=['get'], detail=False, url_path='bind-token')
    def bind_token(self, request, *args, **kwargs):
        """請求綁定TG驗證碼"""
        user = request.user
        telegram_obj = user.telegram
        token = uuid.uuid4().hex
        if not telegram_obj:
            telegram_obj = models.Telegram.objects.create(
                token=token, status=False,
            )
            user.telegram = telegram_obj
            user.save()

        else:
            telegram_obj.token = token
            telegram_obj.status = False
            telegram_obj.save()

        return Response({'token': telegram_obj.token})

    @action(methods=['post'], detail=False, url_path='reset-password')
    def reset_password(self, request, *args, **kwargs):
        """重設密碼"""

        if request.data.get('pass') == request.data.get('checkPass'):
            request.user.set_password(request.data.get('pass'))
            request.user.save()
        else:
            return Response({'message': '重設失敗'}, status=400)

        return Response({'message': '重設成功'})

    @action(methods=['post'], detail=False, url_path='reset-telegram')
    def reset_telegram(self, request, *args, **kwargs):
        """重新綁定TG"""

        telegram_obj = request.user.telegram

        if telegram_obj:
            telegram_obj.status = False
            telegram_obj.save()

        return Response({'message': '取消綁定成功'})

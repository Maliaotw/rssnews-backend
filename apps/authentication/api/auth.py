import logging

from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from authentication import models
from authentication import signals
from authentication.models import ExpiringToken

logger = logging.getLogger(__name__)


class ObtainExpiringAuthToken(ObtainAuthToken):
    """View enabling username/password exchange for expiring token."""
    permission_classes = [permissions.AllowAny]

    model = ExpiringToken

    def post(self, request, *args, **kwargs):
        """Respond to POSTed username/password with token."""
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = ExpiringToken.objects.get_or_create(
                user=user
            )
            self.send_auth_signal(success=True, user=user)

            if token.expired():
                # If the token is expired, generate a new one.
                token.delete()
                token = ExpiringToken.objects.create(
                    user=user
                )

            data = {'token': token.key, 'username': user.username}
            return Response(data)

        else:
            logging.debug('UserLoginView form_invalid')

            # write login failed log
            user = serializer.data['username']
            exist = models.UserProfile.objects.filter(username=user)

            # 如果有帳戶 為密碼錯 , 如無帳戶為帳密錯
            reason = models.UserLoginLog.REASON_PASSWORD if exist else models.UserLoginLog.REASON_NOT_EXIST

            logging.debug(reason)

            self.send_auth_signal(success=False, username=user, reason=reason)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_auth_signal(self, success=True, user=None, username='', reason=''):
        if success:
            logger.debug('send_auth_signal success')
            signals.post_auth_success.send(
                sender=self.__class__, user=user, request=self.request
            )
        else:
            logger.debug('send_auth_signal fail')
            signals.post_auth_failed.send(
                sender=self.__class__, username=username,
                request=self.request, reason=reason
            )

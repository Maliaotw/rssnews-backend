from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from authentication.models import ExpiringToken


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

            if token.expired():
                # If the token is expired, generate a new one.
                token.delete()
                token = ExpiringToken.objects.create(
                    user=user
                )

            data = {'token': token.key, 'username': user.username}
            return Response(data)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

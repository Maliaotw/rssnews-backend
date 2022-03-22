import logging

from rest_framework.response import Response
from src.base.viewset import ModelViewSet

logger = logging.getLogger(__name__)


class HealthzViewSet(ModelViewSet):

    def list(self, request, *args, **kwargs):
        ret = {'code': 200, 'data': [], 'message': f'healthz Hello {request.user}'}
        return Response(ret)





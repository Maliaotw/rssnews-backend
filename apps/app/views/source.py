import logging

from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from app import models
from app import serializers
from authentication.permissions import IsAppUser, IsValidUser
from src.base.viewset import ModelViewSet

logger = logging.getLogger(__name__)

class SourceViewSet(ModelViewSet):
    model_class = models.Source
    queryset = model_class.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAppUser | IsValidUser,)

    serializer_action_classes = {
        'list': serializers.SourceListSerializer,
        'create': serializers.SourceCreateSerializer,
        'update': serializers.SourceListSerializer,
        'retrieve': serializers.SourceListSerializer
    }

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def tree(self, request, *args, **kwargs):
        """Tree 訂閱列表"""
        category = serializers.CategoryListSerializer(models.Category.objects.all(), many=True).data
        sub = [i.id for i in request.user.sourse.all()]

        return Response({'category': category, 'sub': sub})


    @action(detail=False)
    def refresh(self, request, *args, **kwargs):
        return super().refresh(request, *args, **kwargs)

    @refresh.mapping.post
    def refresh_post(self, request, *args, **kwargs):
        """來源初始化

        """
        from app.management.commands.initialize_data import initialize_data
        initialize_data()

        return Response({'code': 200, 'message': '刷新成功'})

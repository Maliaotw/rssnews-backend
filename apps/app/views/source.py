import logging

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from app import models
from app import serializers
from app.filters import SourceListFilter
from authentication.permissions import IsAppUser, IsValidUser, AllowAny
from src.base.viewset import ModelViewSet
from src.base.pagination import LimitOffsetPagination, PageNumberPagination
from src.feedparser.parse import parse

logger = logging.getLogger(__name__)


class SourceViewSet(ModelViewSet):
    model_class = models.Source
    queryset = model_class.objects.filter(is_deleted=False)
    # pagination_class = PageNumberPagination
    permission_classes = (IsAppUser | IsValidUser,)
    filterset_class = SourceListFilter

    permission_classes_mapping = {
        'list': (AllowAny,),
        'selects': (AllowAny,),
        'tree': (AllowAny,),
    }

    serializer_action_classes = {
        'list': serializers.SourceListSerializer,
        'create': serializers.SourceCreateSerializer,
        'update': serializers.SourceCreateSerializer,
        'retrieve': serializers.SourceDetailSerializer
    }

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def selects(self, request: Request, *args, **kwargs):
        data = {
            'category': list(models.Category.objects.filter(is_deleted=False).values('id', 'name')),
            'enable': [{'id': 0, 'name': '否'}, {'id': 1, 'name': '是'}]
        }
        return Response(data)

    @action(methods=['get'], detail=False)
    def tree(self, request, *args, **kwargs):
        """Tree 訂閱列表"""
        _user = request.user
        category = serializers.CategoryListSerializer(models.Category.objects.all(), many=True).data
        if _user.username:

            sub = [i.id for i in request.user.sourse.all()]
            username = _user.username

        else:
            sub = []
            username = ''

        return Response({'category': category, 'sub': sub, 'username': username})

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

    @action(methods=['post'], detail=False)
    def check_source(self, request, *args, **kwargs):
        """確認來源是否可用, 返回最新一筆文章

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        url = request.data.get('url')
        if not url:
            return Response({'code': 100, 'message': 'url參數未輸入'})

        feed = parse(url)
        if not feed.feed:
            return Response({'code': 100, 'message': ''})

        # logger.info(feed.entries)
        _result = feed.entries[0]
        result = {
            'title': _result['title'],
            'source': feed.feed.title,
            'summary': _result['summary'],
            'published_datetime': _result['published_datetime'],
            'updated_datetime': _result['updated_datetime'],
        }

        return Response({'code': 200, 'message': '刷新成功', 'result': result})

    @action(methods=['post'], detail=False)
    def batch_enable(self,  request, *args, **kwargs):
        """批量啟用"""
        pass

    @action(methods=['post'], detail=False)
    def batch_deleted(self,  request, *args, **kwargs):
        """批量刪除"""
        pass

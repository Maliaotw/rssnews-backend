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
            'enable': [{'id': 0, 'name': '否'}, {'id': 1, 'name': '是'}],
            'subscription': [{'id': 0, 'name': '否'}, {'id': 1, 'name': '是'}],
            'bacth_edit': [{'value': 'subscription', 'label': '訂閱'}]
        }

        # if 管理員  批量編輯選項
        if request.user.is_superuser:
            data['bacth_edit'].append({'value': 'enable', 'label': '啟用'})

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
        """確認來源是否可用, 返回最新5筆文章

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        url = request.data.get('url')
        if not url:
            return self.warning_info(message='url參數未輸入.')

        feed = parse(url)
        if not feed.feed:
            return self.warning_info(message='該鏈接可能已失效, 找不到返回信息.')

        _result = []
        # logger.info(feed.entries)
        for i in feed.entries:
            _result.append(f"{i['published_datetime']} {i['title']}")
        # _result = feed.entries[0]
        # result = {
        #     'title': _result['title'],
        #     'source': feed.feed.title,
        #     'summary': _result['summary'],
        #     'published_datetime': _result['published_datetime'],
        #     'updated_datetime': _result['updated_datetime'],
        # }
        if not _result:
            return self.warning_info(message='該鏈接可能已失效, 找不到返回信息.')
        else:

            return self.success_info(message='測試成功', result=_result[:10])

    @action(methods=['post'], detail=False)
    def batch_enable(self, request, *args, **kwargs):
        """批量啟用

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        ids = request.data.get('ids')
        if not ids:
            return Response({'code': 100, 'message': '參數不對, ids未輸入'})

        objs = self.model_class.objects.filter(id__in=ids, is_deleted=False)
        objs.update(enable=1)
        return Response({'code': 200, 'message': '批量修改成功', 'result': {}})

    @action(methods=['post'], detail=False)
    def batch_deleted(self, request, *args, **kwargs):
        """批量刪除"""

        if not request.user.is_superuser:
            return Response({'code': 400, 'message': '無操作權限'})

        ids = request.data.get('ids')
        if not ids:
            return Response({'code': 100, 'message': '參數不對, ids未輸入'})

        objs = self.model_class.objects.filter(id__in=ids, is_deleted=False)
        objs.update(is_deleted=True)
        return Response({'code': 200, 'message': '批量刪除成功', 'result': {}})

    @action(methods=['post'], detail=False)
    def batch_edit(self, request, *args, **kwargs):
        """批量修改狀態, 啟用|訂閱

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ids = request.data.get('ids')
        field = request.data.get('field')
        to = request.data.get('to')

        if not ids:
            return Response({'code': 100, 'message': '參數不對, ids未輸入'})

        if not field:
            return Response({'code': 100, 'message': '參數不對, field未輸入'})

        if to is None:
            return Response({'code': 100, 'message': '參數不對, to未輸入'})

        if not request.user.is_superuser:
            if field in ['enable']:
                return Response({'code': 400, 'message': '無操作權限'})

        objs = self.model_class.objects.filter(id__in=ids, is_deleted=False)

        if field == 'subscription':
            if to == 0:
                for i in objs:
                    self.request.user.sourse.remove(i)
            elif to == 1:
                for i in objs:
                    self.request.user.sourse.add(i)

        else:
            objs.update(**{f'{field}': to})

        return Response({'code': 200, 'message': '批量修改成功', 'result': {}})

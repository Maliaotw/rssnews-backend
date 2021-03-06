import datetime
import json
import logging
import os.path
import re

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from app import models
from app import serializers
from app.filters import NewsListFilter
from authentication.permissions import IsAppUser, IsValidUser
from src.base.viewset import ModelViewSet
from src.telegram.bot import Bot
from dateutil.parser import parse

logger = logging.getLogger(__name__)


class NewsViewSet(ModelViewSet):
    model_class = models.News
    queryset = model_class.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsValidUser | IsAppUser,)
    filterset_class = NewsListFilter

    serializer_action_classes = {
        'list': serializers.NewsListSerializer,
        'create': serializers.NewsCreateSerializer,
        'update': serializers.NewsUpdateSerializer,
        'retrieve': serializers.NewsDetailSerializer
    }

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def selects(self, request: Request, *args, **kwargs):
        category = request.query_params.get('category')
        if category:
            return Response(
                serializers.SourceSelectsSerializer(models.Source.objects.filter(category=category), many=True).data)
        else:
            return Response(serializers.CategorySelectsSerializer(models.Category.objects.all(), many=True).data)

    @action(detail=False)
    def refresh(self, request, *args, **kwargs):
        return super().refresh(request, *args, **kwargs)

    @refresh.mapping.post
    def refresh_post(self, request, *args, **kwargs):
        """??????

        """
        from config.settings.base import STATIC_DIR

        data = json.load(open(os.path.join(STATIC_DIR, 'tmp', 'news.json'), 'r'))
        # print(data)
        for news_data in data:
            news_data['id'] = news_data.pop('md5')
            tag = news_data.pop('tag')

            if news_data.get('source_id'):
                news_data['source'] = news_data.pop('source_id')

            news_data['published_parsed'] = parse(news_data['published_parsed'])
            news_data['updated_parsed'] = parse(news_data['updated_parsed'])

            s = serializers.NewsCreateSerializer(data=news_data)
            if not s.is_valid():
                continue

            obj = s.save()

            for i in tag:
                t, created = models.Tag.objects.get_or_create(name=i)
                obj.tag.add(t)

            # self.redis.hdel('push', key)
        return Response('ok')

    @action(detail=False)
    def cache(self, request, *args, **kwargs):
        return super().cache(request, *args, **kwargs)

    @cache.mapping.post
    def cache_post(self, request, *args, **kwargs):
        """??????

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        from src.utils.rss import News, Source
        from config.settings.base import STATIC_DIR

        name = self.request.data.get('name')
        if name:
            sourece_objs = models.Source.objects.filter(name=name)
        else:
            sourece_objs = models.Source.objects.all()

        data_list = []

        for source_obj in sourece_objs:
            source = Source(
                id=source_obj.id,
                name=source_obj.name,
                thumbnail=source_obj.thumbnail,
                url=source_obj.url,
                category=source_obj.category_id,
                remarks=source_obj.remarks,
                timezone=source_obj.timezone,
                status=source_obj.status
            )
            if not source_obj.thumbnail:
                source_obj.thumbnail = source.source_thumbnail
                source_obj.save()

            new = News(source)
            new.run()
            data_list.extend(new.result)

        json.dump(
            data_list,
            open(os.path.join(STATIC_DIR, 'tmp', 'news.json'), 'w'),
            indent=4,
            sort_keys=True,
            default=str
        )

        return Response({'code': 200, 'message': '????????????'})

    def _dict_to_msg_text(self, data):
        txt = [
            "??????:\n%s" % data.get('name', ''),
            "????????????:%s" % data.get('published_parsed', ''),
            "??????:%s" % [],
            "??????:%s" % data.get('source', ''),
            "??????:\n%s" % re.sub(r'</?\w+[^>]*>', '', data.get('content', '')[:150]),
            "??????:\n%s" % data.get('url', '')
        ]
        return "\n".join(txt)

    def _dict_to_email_text(self, data):
        txt = [
            "??????:\n%s" % data.get('name', ''),
            "????????????:%s" % data.get('published_parsed', ''),
            "??????:%s" % [],
            "??????:%s" % data.get('source', ''),
            "??????:\n%s" % data.get('content', ''),
            "??????:\n%s" % data.get('url', '')
        ]
        return "\n".join(txt)

    @action(methods=['post'], detail=False)
    def push(self, request, *args, **kwargs):
        # ????????????bot
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

        # # ????????????MailUser
        # email_admin = models.EmailMaster.objects.filter(user=conf.EMAILUSER['user'])
        #
        # if email_admin:
        #     email_admin = email_admin.first()
        # else:
        #     email_admin = models.EmailMaster.objects.create(**conf.EMAILUSER)

        # ?????????????????????
        activate_user = models.Telegram.objects.filter(status=True)

        logger.info(activate_user)

        news_objs = models.News.objects.filter(push_status=False)

        for news in news_objs:

            logger.info(news)

            # Source ?????????
            sub_user = news.source.userprofile.all()
            logger.info(sub_user)

            # ???TG??????????????????
            tg_sub_user = sub_user.filter(telegram__in=activate_user)

            logger.info(sub_user)

            news_data = {
                'name': news.name,
                'source': news.source.name,
                'published_parsed': (news.published_parsed + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
                'tag': [],
                'content': news.content,
                'url': news.url
            }

            tg_text = self._dict_to_msg_text(news_data)
            email_text = self._dict_to_email_text(news_data)

            # ??????TG??????
            msg = bot.send_message(chat_id=settings.TELEGRAM_CHANNEL_ID, text=tg_text)

            # ????????????????????????TG
            for user in tg_sub_user:
                logger.info(user)
                bot.forward_message(
                    chat_id=user.telegram.chat_id,
                    from_chat_id=settings.TELEGRAM_CHANNEL_ID,
                    message_id=msg['message_id']
                )

            # ?????????????????????
            logger.info(sub_user)
            toaddrs = list(filter(None, [user.email for user in sub_user]))
            logger.info(toaddrs)

            # if toaddrs:
            #     smtp = smtphelper(host=email_admin.host, port=email_admin.port, user=email_admin.user, pwd=email_admin.passwd)
            #     smtp.smtp_sendhtml(news.name,email_text,toaddrs=toaddrs)

            # ???????????? ?????????
            news.push_status = True
            news.save()

        return Response({'code': 200, 'message': '????????????', 'result': {}})

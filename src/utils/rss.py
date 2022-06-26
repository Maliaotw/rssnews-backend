# from utils import request, watermark
import hashlib
import logging
import os
import re
import time
from dataclasses import dataclass

import feedparser
from dateutil import parser
from django.conf import settings
from imgurpython import ImgurClient

# import telegram
# from typing import List, Dict
from . import watermark
from config.settings.base import redis
import json

from ..feedparser.parse import parse

logger = logging.getLogger(__name__)


@dataclass
class Source:
    id: int
    name: str
    thumbnail: str
    url: str
    category: str
    remarks: str
    timezone: int
    status: bool

    def md5(self):

        # MD5
        m = hashlib.md5()
        m.update(self.name.encode("utf-8"))
        h = m.hexdigest()
        return h

    def push_imgur(self, filename):
        # 連接
        client = ImgurClient(settings.IMGUR_ID, settings.IMGUR_SECRET)
        try:
            text = client.upload_from_path(filename)
            returnlink = str(text['link'])
            return returnlink

        except Exception as e:
            logger.error(e, exc_info=True)
            return ''

    @property
    def source_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail

        filename = os.path.join(settings.IMAGE_DIR, "%s.jpg" % self.md5())
        # filename = os.path.join(settings.MEDIA_ROOT, 'image', "%s.jpg" % self.md5())
        if not os.path.exists(filename):
            logger.info(f'{self.name}, 創建檔案')
            watermark.str2img(txt=self.name, path=filename)

        return self.push_imgur(filename)


class Feed:

    def __init__(self, source: Source):
        # print(source)
        self.source = source
        self.news_list = []

    def _crawl(self):
        feed = parse(self.source.url)
        # logger.debug(feed)

        # 判斷網址如果失效, 不返回資料
        post = feed.entries
        if post:
            return post

    def clean(self, data):
        # 過濾有summary的資料
        logger.info(f'source: {self.source.name}')
        if not data:
            logger.warning(f'source: {self.source.name} 沒資料')
            return

        data = filter(lambda x: x.get('summary'), data)

        for post in data:

            tag = [t['term'] for t in post.tags] if post.get('tags') else []

            # 正則解出縮圖URL
            thumbnail_obj = re.findall(r'((http(s?):)([/|.|\w|\s|-])*.(?:jpg|gif|png))', post.get('summary', ''))
            if thumbnail_obj:
                thumbnail = thumbnail_obj[0][0]
            else:
                thumbnail = self.source.thumbnail
            #
            # if post.published_parsed:
            #     published_parsed = time.strftime("%Y/%m/%d %H:%M:%S", post.published_parsed)
            # else:
            #     published_parsed = parser.parse(post.published)
            #
            # if post.updated_parsed:
            #     updated_parsed = time.strftime("%Y/%m/%d %H:%M:%S", post.updated_parsed)
            # else:
            #     updated_parsed = published_parsed

            data = {
                'source': self.source.id,
                'name': post.get('title'),
                'url': post.get('feedburner_origlink') if post.get('feedburner_origlink') else post.link,
                # 'publish': post.get('published', ''),
                # 'published_parsed': published_parsed,
                # 'updated_parsed': updated_parsed,
                'published_parsed': post.published_datetime,
                'updated_parsed': post.updated_datetime,
                'content': post.summary,
                'tag': tag,
                'thumbnail': thumbnail,
            }
            self.news_list.append(data)

    def run(self):
        _data = self._crawl()
        self.clean(_data)
        return self.news_list


class News:

    def __init__(self, source: Source):
        self.source = source
        self.result = []
        self.result_data = []

    def get_crawl(self):
        logger.info(f'get_crawl, {self.source}')
        feed = Feed(self.source)
        feed.run()
        return feed.news_list

    def md5(self, name):
        """MD5"""
        m = hashlib.md5()
        m.update(name.encode("utf-8"))
        h = m.hexdigest()
        return h

    def run(self, debug=False):
        self.data = self.get_crawl()
        # print(self.data)
        for data in self.data:
            name = self.md5(f'{data["name"]}{data["url"]}')
            data['md5'] = name
            data['source_name'] = self.source.name

            _data = json.dumps(data, indent=4, sort_keys=True, default=str)
            self.result.append(data)

            # 先檢查是否入庫, 入庫會存md5到db的key, 先比對在儲存到cache
            # redis.srem('db', name)
            if debug or not redis.sismember('db', name):
                redis.hset('news', name, _data)

        return self.result_data

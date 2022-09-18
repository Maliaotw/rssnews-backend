import time

import feedparser
from dateutil import parser
from datetime import timedelta, datetime


def parse(url: str) -> feedparser.FeedParserDict:
    _data: feedparser.FeedParserDict = feedparser.parse(url)
    _feed = _data.get('feed')

    if not _feed:
        return _data

    for post in _data.entries:
        post: feedparser.FeedParserDict

        if post.published_parsed:
            # post.published_parsed = time.strftime("%Y/%m/%d %H:%M:%S", post.published_parsed)
            published_datetime = datetime(*post.published_parsed[:6]) + timedelta(hours=8)
            # post['published_datetime'] = published_datetime.strftime("%Y/%m/%d %H:%M:%S")

            # 如果發布時間大於當前時間, 不做任何處理
            if published_datetime > datetime.now():
                published_datetime = datetime(*post.published_parsed[:6])
        else:
            published_datetime = parser.parse(post.published)

        post['published_datetime'] = published_datetime.strftime("%Y/%m/%d %H:%M:%S")

        if post.updated_parsed:
            # updated_datetime = time.strftime("%Y/%m/%d %H:%M:%S", post.updated_parsed)
            updated_datetime = datetime(*post.updated_parsed[:6]) + timedelta(hours=8)
        else:
            updated_datetime = published_datetime

        post['updated_datetime'] = updated_datetime.strftime("%Y/%m/%d %H:%M:%S")

    return _data

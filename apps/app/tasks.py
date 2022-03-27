# from celery import shared_task, Task, subtask
import logging

from celery import shared_task
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from app.views.news import NewsViewSet

logger = logging.getLogger(__name__)


@shared_task
def add(x, y):
    return str(x + y)


@shared_task
def crawl_news():
    """爬取RSS

    :return:
    """
    path = '/api/v1/news/cache/'
    mothod = 'post'
    data = {}

    factory = APIRequestFactory()
    request = factory.post(path, data=None,content_type='text/plain')  # WSGIRequest
    request = Request(request)  # rest_framework.request.Request

    # Add the view call to get response object
    viewset = NewsViewSet()
    viewset.request = request
    response = viewset.cache_post(request)

    return response.data

@shared_task
def sync_news():
    """將新聞入庫到DB

    :return:
    """
    path = '/api/v1/news/refresh/'
    mothod = 'post'
    data = {}

    factory = APIRequestFactory()
    request = factory.post(path, data=None,content_type='text/plain')  # WSGIRequest
    request = Request(request)  # rest_framework.request.Request

    # Add the view call to get response object
    viewset = NewsViewSet()
    viewset.request = request
    response = viewset.refresh_post(request)

    return response.data


@shared_task
def send_news():
    """寄送TG或電郵

    :return:
    """
    path = '/api/v1/news/push/'
    mothod = 'post'
    data = {}

    factory = APIRequestFactory()
    request = factory.post(path, data=None,content_type='text/plain')  # WSGIRequest
    request = Request(request)  # rest_framework.request.Request

    # Add the view call to get response object
    viewset = NewsViewSet()
    viewset.request = request
    response = viewset.push(request)

    return response.data



from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from authentication import api

app_name = 'authentication'

# viewset 配置路由
router = DefaultRouter()
router.register(r'loginlog', api.LoginListViewSet)  # Allow: GET, POST, HEAD, OPTIONS


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', api.ObtainExpiringAuthToken.as_view()),
]

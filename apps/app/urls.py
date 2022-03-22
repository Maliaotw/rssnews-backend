from django.contrib.auth.decorators import login_required, permission_required
from django.urls import include, path
# from rest_framework_expiring_authtoken.views import ObtainExpiringAuthToken
from authentication.views import ObtainExpiringAuthToken
from rest_framework import routers
from . import views

app_name = 'app'

router = routers.DefaultRouter()
router.register('healthz', views.HealthzViewSet, 'healthz')
router.register('news', views.NewsViewSet, 'news')
router.register('category', views.CategoryViewSet, 'category')
router.register('source', views.SourceViewSet, 'source')
router.register('userprofile', views.UserProfileViewSet, 'userprofile')
router.register('registrations', views.RegistrationViewSet, 'registrations')

api_v1 = [
    path('api-token-auth/', ObtainExpiringAuthToken.as_view()),
]

api_v1 += router.urls

urlpatterns = [
    path('v1/', include(api_v1)),
]

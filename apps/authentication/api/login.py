from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from authentication import models
from authentication import serializers


class LoginFilter(filters.FilterSet):
    username = filters.CharFilter(lookup_expr='contains')
    datetime = filters.DateTimeFromToRangeFilter(label='datetime')

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(datetime__range=self.data.getlist('datetime[]'))

    class Meta:
        model = models.UserLoginLog
        fields = ('username', 'status', 'datetime')


class LoginListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.UserLoginLog.objects.all()
    serializer_class = serializers.LoginSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LoginFilter

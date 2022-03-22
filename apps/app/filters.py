from django_filters import FilterSet, filters
from .models import News


class NewsListFilter(FilterSet):

    name = filters.CharFilter(lookup_expr='contains')
    category = filters.CharFilter(field_name='source__category__id')

    class Meta:
        model = News
        fields = ['name', 'source', 'category']




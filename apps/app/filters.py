from django_filters import FilterSet, filters
from .models import News, Source


class NewsListFilter(FilterSet):

    name = filters.CharFilter(lookup_expr='contains')
    category = filters.CharFilter(field_name='source__category__id')

    class Meta:
        model = News
        fields = ['name', 'source', 'category']



class SourceListFilter(FilterSet):

    name = filters.CharFilter(lookup_expr='contains')
    category = filters.CharFilter(field_name='category__id')
    enable = filters.CharFilter()

    class Meta:
        model = Source
        fields = ['name', 'category', 'enable']

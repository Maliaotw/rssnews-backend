import logging

from app import models
from app import serializers
from src.base.viewset import ModelViewSet

logger = logging.getLogger(__name__)


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategoryListSerializer
    model_class = models.Category
    queryset = model_class.objects.all()

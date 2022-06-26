
from rest_framework.settings import api_settings

from rest_framework.viewsets import ModelViewSet


class GetPermissionClassMix:
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    permission_classes_mapping = {

    }

    def check_permissions(self, request):
        self.permission_classes = self.permission_classes_mapping.get(
            self.action,
            self.permission_classes
        )

        super().check_permissions(request)


class GetSerializerClassMixin:
    serializer_action_classes = {

    }

    def get_serializer_class(self):
        """
        A class which inhertis this mixins should have variable
        `serializer_action_classes`.
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:
        class SampleViewSet(viewsets.ViewSet):
            serializer_class = DocumentSerializer
            serializer_action_classes = {
               'upload': UploadDocumentSerializer,
               'download': DownloadDocumentSerializer,
            }
            @action
            def upload:
                ...
        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class ModelViewSet(GetPermissionClassMix, GetSerializerClassMixin, ModelViewSet):

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

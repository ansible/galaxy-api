from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.settings import api_settings

from galaxy_api.api import models, permissions
from galaxy_api.api.ui import serializers


class NamespaceViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = "name"
    serializer_class = serializers.NamespaceSerializer
    queryset = models.Namespace.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        permissions.IsNamespaceOwnerOrReadOnly
    ]

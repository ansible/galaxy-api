import galaxy_pulp
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.settings import api_settings
from rest_framework.response import Response

from galaxy_api.api import models
from galaxy_api.api.ui import serializers
from galaxy_api.common import pulp


class CollectionViewSet(viewsets.GenericViewSet):
    lookup_url_kwarg = 'collection'
    lookup_value_regex = r'[0-9a-z_]+/[0-9a-z_]+'

    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def list(self, request, *args, **kwargs):
        self.paginator.from_request(request)

        page = (self.paginator.offset // self.paginator.limit) + 1
        page_size = self.paginator.limit

        api = galaxy_pulp.PulpCollectionsApi(pulp.get_client())

        response = api.list(is_highest=True, page=page, page_size=page_size)
        self.paginator.count = response.count

        namespaces = set(collection['namespace'] for collection in response.results)
        namespaces = self._query_namespaces(namespaces)

        data = serializers.CollectionSerializer(
            response.results, many=True, context={'namespace_dict': namespaces}
        ).data

        return self.paginator.get_paginated_response(data)

    def retrieve(self, request, *args, **kwargs):
        namespace, name = self.kwargs['collection'].split('/')
        namespace_obj = get_object_or_404(models.Namespace, name=namespace)

        api = galaxy_pulp.PulpCollectionsApi(pulp.get_client())
        # TODO: When limit offset pagination lands to pulp add limit=1
        response = api.list(namespace=namespace, name=name, is_highest=True)
        if not response.results:
            raise NotFound()

        data = serializers.CollectionSerializer(
            response.results[0], context={'namespace': namespace_obj}
        ).data

        return Response(data)

    def set_deprecated(self):
        pass

    @staticmethod
    def _query_namespaces(names):
        queryset = models.Namespace.objects.filter(name__in=names)
        namespaces = {ns.name: ns for ns in queryset}
        return namespaces


class CollectionVersionViewSet(viewsets.ViewSet):
    lookup_url_kwarg = 'version'
    lookup_value_regex = r'[0-9A-Za-z.+-]+'

    def list(self, request, *args, **kwargs):
        namespace, name = self.kwargs['collection'].split('/')

        api = galaxy_pulp.PulpCollectionsApi(pulp.get_client())

        response = api.list(namespace=namespace, name=name)
        if response.count == 0:
            raise NotFound()

        data = serializers.CollectionVersionBaseSerializer(response.results, many=True).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        namespace, name = self.kwargs['collection'].split('/')
        version = self.kwargs['version']

        api = galaxy_pulp.PulpCollectionsApi(pulp.get_client())

        response = api.list(namespace=namespace, name=name, version=version)
        if not response.results:
            raise NotFound()

        data = serializers.CollectionVersionSerializer(response.results[0]).data
        return Response(data)


class CollectionImportViewSet(viewsets.ViewSet):
    lookup_url_kwarg = 'id'

    def list(self, request, *args, **kwargs):
        api_client = pulp.get_client()
        api = galaxy_pulp.PulpImportsApi(api_client)

        result = api.list(**self.request.query_params)

        return Response(result)

    def retrieve(self, request, *args, **kwargs):
        api_client = pulp.get_client()
        api = galaxy_pulp.PulpImportsApi(api_client)

        result = api.get(id=self.kwargs['id'])

        return Response(result)

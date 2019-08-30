import galaxy_pulp
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action as drf_action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from galaxy_api.api import models
from galaxy_api.api.ui import serializers
from galaxy_api.common import pulp


class CollectionViewSet(viewsets.GenericViewSet):
    lookup_url_kwarg = 'collection'
    lookup_value_regex = r'[0-9a-z_]+/[0-9a-z_]+'

    def list(self, request, *args, **kwargs):
        self.paginator.init_from_request(request)

        params = self.request.query_params.dict()
        params.update({
            'offset': self.paginator.offset,
            'limit': self.paginator.limit,
        })

        api = galaxy_pulp.PulpCollectionsApi(pulp.get_client())
        response = api.list(is_highest=True, **params)

        namespaces = set(collection['namespace'] for collection in response.results)
        namespaces = self._query_namespaces(namespaces)

        data = serializers.CollectionListSerializer(
            response.results, many=True, context={'namespaces': namespaces}
        ).data
        return self.paginator.paginate_proxy_response(data, response.count)

    def retrieve(self, request, *args, **kwargs):
        namespace, name = self.kwargs['collection'].split('/')
        namespace_obj = get_object_or_404(models.Namespace, name=namespace)

        api = galaxy_pulp.PulpCollectionsApi(pulp.get_client())
        # TODO: When limit offset pagination lands to pulp add limit=1
        response = api.list(namespace=namespace, name=name, is_highest=True)
        if not response.results:
            raise NotFound()

        data = serializers.CollectionDetailSerializer(
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


class CollectionVersionViewSet(viewsets.GenericViewSet):
    lookup_url_kwarg = 'version'
    lookup_value_regex = r'[0-9A-Za-z.+-]+'

    def list(self, request, *args, **kwargs):
        namespace, name = self.kwargs['collection'].split('/')

        self.paginator.init_from_request(request)

        params = self.request.query_params.dict()
        params.update({
            'offset': self.paginator.offset,
            'limit': self.paginator.limit,
        })

        api = galaxy_pulp.PulpCollectionsApi(pulp.get_client())
        response = api.list(namespace=namespace, name=name, **params)
        if response.count == 0:
            raise NotFound()

        data = serializers.CollectionVersionBaseSerializer(response.results, many=True).data
        return self.paginator.paginate_proxy_response(data, response.count)

    def retrieve(self, request, *args, **kwargs):
        namespace, name = self.kwargs['collection'].split('/')
        version = self.kwargs['version']

        api = galaxy_pulp.PulpCollectionsApi(pulp.get_client())
        response = api.list(namespace=namespace, name=name, version=version, limit=1)
        if not response.results:
            raise NotFound()

        data = serializers.CollectionVersionSerializer(response.results[0]).data
        return Response(data)

    @drf_action(methods=["PUT", "DELETE"], detail=True, url_path="certified")
    def set_certified(self, request, *args, **kwargs):
        namespace, name = self.kwargs['collection'].split('/')
        version = self.kwargs['version']

        api = galaxy_pulp.GalaxyCollectionVersionsApi(pulp.get_client())

        if self.request.method == "PUT":
            api_method = api.set_certified
        else:
            api_method = api.unset_certified

        response = api_method(
            prefix=settings.API_PATH_PREFIX,
            namespace=namespace,
            name=name,
            version=version,
        )
        return Response(response)


class CollectionImportViewSet(viewsets.GenericViewSet):
    lookup_url_kwarg = 'id'

    def list(self, request, *args, **kwargs):
        self.paginator.init_from_request(request)

        params = self.request.query_params.dict()
        params.update({
            'offset': self.paginator.offset,
            'limit': self.paginator.limit,
        })

        api_client = pulp.get_client()
        api = galaxy_pulp.PulpImportsApi(api_client)

        response = api.list(**params)

        return self.paginator.paginate_proxy_response(response.results, response.count)

    def retrieve(self, request, *args, **kwargs):
        api_client = pulp.get_client()
        api = galaxy_pulp.PulpImportsApi(api_client)

        result = api.get(id=self.kwargs['id'])

        return Response(result)

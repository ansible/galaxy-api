# Copyright 2019 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json

import requests
from django.conf import settings
import galaxy_pulp
from django.core.exceptions import ValidationError
from django.http import StreamingHttpResponse, HttpResponseRedirect
from rest_framework import views
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.settings import api_settings

from galaxy_api.api.models import Namespace
from galaxy_api.api.v3.serializers import CollectionUploadSerializer
from galaxy_api.common import pulp
from galaxy_api.api import permissions, models

import logging
log = logging.getLogger(__name__)


class CollectionViewSet(viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        self.paginator.init_from_request(request)

        params = self.request.query_params.dict()
        params.update({
            'offset': self.paginator.offset,
            'limit': self.paginator.limit,
        })

        api = galaxy_pulp.GalaxyCollectionsApi(pulp.get_client())
        response = api.list(prefix=settings.API_PATH_PREFIX, **params)
        return self.paginator.paginate_proxy_response(response.results, response.count)

    def retrieve(self, request, *args, **kwargs):
        api = galaxy_pulp.GalaxyCollectionsApi(pulp.get_client())
        response = api.get(
            prefix=settings.API_PATH_PREFIX,
            namespace=self.kwargs['namespace'],
            name=self.kwargs['name']
        )
        return Response(response)


class CollectionVersionViewSet(viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        self.paginator.init_from_request(request)

        params = self.request.query_params.dict()
        params.update({
            'offset': self.paginator.offset,
            'limit': self.paginator.limit,
        })

        api = galaxy_pulp.GalaxyCollectionVersionsApi(pulp.get_client())
        response = api.list(
            prefix=settings.API_PATH_PREFIX,
            namespace=self.kwargs['namespace'],
            name=self.kwargs['name'],
            **params,
        )

        # Consider an empty list of versions as a 404 on the Collection
        if not response.results:
            raise NotFound()

        return self.paginator.paginate_proxy_response(response.results, response.count)

    def retrieve(self, request, *args, **kwargs):
        api = galaxy_pulp.GalaxyCollectionVersionsApi(pulp.get_client())
        response = api.get(
            prefix=settings.API_PATH_PREFIX,
            namespace=self.kwargs['namespace'],
            name=self.kwargs['name'],
            version=self.kwargs['version'],
        )
        response['download_url'] = request.build_absolute_uri(response['download_url'])
        return Response(response)


class CollectionImportViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):
        api = galaxy_pulp.GalaxyImportsApi(pulp.get_client())
        response = api.get(prefix=settings.API_PATH_PREFIX, id=pk)
        return Response(response.to_dict())


class CollectionArtifactUploadView(views.APIView):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        permissions.IsNamespaceOwner,
    ]

    def post(self, request, *args, **kwargs):
        serializer = CollectionUploadSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        filename = data['filename']

        try:
            namespace = Namespace.objects.get(name=filename.namespace)
        except Namespace.DoesNotExist:
            raise ValidationError(
                'Namespace "{0}" does not exist.'.format(filename.namespace)
            )

        self.check_object_permissions(request, namespace)

        api = pulp.get_client()
        url = '{host}/{prefix}{path}'.format(
            host=api.configuration.host,
            prefix=settings.API_PATH_PREFIX,
            path='/v3/artifacts/collections/',
        )

        post_params = self._prepare_post_params(data)
        try:
            upload_response = api.request(
                'POST',
                url,
                headers={'Content-Type': 'multipart/form-data'},
                post_params=post_params,
            )
        except galaxy_pulp.ApiException:
            log.exception('Failed to publish artifact %s (namespace=%s, sha256=%s) to pulp at url=%s',  # noqa
                          data['file'].name, namespace, data.get('sha256'), url)
            raise

        upload_response_data = json.loads(upload_response.data)

        task_detail = api.call_api(
            upload_response_data['task'],
            'GET',
            auth_settings=['BasicAuth'],
            response_type='CollectionImport',
            _return_http_data_only=True,
        )

        log.info('Publishing of artifact %s to namespace=%s by user=%s created pulp import task_id=%s', # noqa
                 data['file'].name, namespace, request.user, task_detail.id)

        models.CollectionImport.objects.create(
            task_id=task_detail.id,
            created_at=task_detail.created_at,
            namespace=namespace,
            name=data['filename'].name,
            version=data['filename'].version,
        )

        return Response(data=upload_response_data, status=upload_response.status)

    @staticmethod
    def _prepare_post_params(data):
        filename = data['filename']
        post_params = [
            ('file', (data['file'].name, data['file'].read(), data['mimetype'])),
            ('expected_namespace', filename.namespace),
            ('expected_name', filename.name),
            ('expected_version', filename.version),
        ]
        if data['sha256']:
            post_params.append(('sha256', data['sha256']))
        return post_params


class CollectionArtifactDownloadView(views.APIView):
    def get(self, request, *args, **kwargs):
        # NOTE(cutwater): Using urllib3 because it's already a dependency of pulp_galaxy
        url = 'http://{host}:{port}/{prefix}/automation-hub/{filename}'.format(
            host=settings.PULP_CONTENT_HOST,
            port=settings.PULP_CONTENT_PORT,
            prefix=settings.PULP_CONTENT_PATH_PREFIX.strip('/'),
            filename=self.kwargs['filename'],
        )
        response = requests.get(url, stream=True, allow_redirects=False)

        if response.status_code == requests.codes.not_found:
            raise NotFound()

        if response.status_code == requests.codes.found:
            return HttpResponseRedirect(response.headers['Location'])

        if response.status_code == requests.codes.ok:
            return StreamingHttpResponse(
                response.iter_content(chunk_size=4096),
                content_type=response.headers['Content-Type']
            )

        raise APIException('Unexpected response from content app. '
                           f'Code: {response.status_code}.')

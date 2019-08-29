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
import mimetypes

from django.conf import settings
import galaxy_pulp
from rest_framework.response import Response
from rest_framework import viewsets

from galaxy_api.common import pulp


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
        return self.paginator.paginate_proxy_response(response.results, response.count)

    def retrieve(self, request, *args, **kwargs):
        api = galaxy_pulp.GalaxyCollectionVersionsApi(pulp.get_client())
        response = api.get(
            prefix=settings.API_PATH_PREFIX,
            namespace=self.kwargs['namespace'],
            name=self.kwargs['name'],
            version=self.kwargs['version'],
        )
        return Response(response)


class CollectionArtifactViewSet(viewsets.ViewSet):

    def upload(self, request, *args, **kwargs):
        # TODO: Validate namespace
        # TODO: Validate namespace permissions

        file = request.data['file']
        mimetype = (mimetypes.guess_type(file.name)[0] or 'application/octet-stream')
        post_params = [
            ('file', (file.name, file.read(), mimetype))
        ]

        sha256 = request.data.get('sha256')
        if sha256:
            post_params.append(('sha256', sha256))

        api = pulp.get_client()
        url = '{host}/{prefix}{path}'.format(
            host=api.configuration.host,
            prefix=settings.API_PATH_PREFIX,
            path='/v3/artifacts/collections/',
        )
        try:
            response = api.request(
                'POST',
                url,
                headers={'Content-Type': 'multipart/form-data'},
                post_params=post_params,
            )
        except galaxy_pulp.ApiException as exc:
            status = exc.status
            data = exc.body
            headers = exc.headers
        else:
            status = response.status
            data = response.data
            headers = response.getheaders()

        if headers['Content-Type'] == 'application/json':
            data = json.loads(data)
        return Response(data=data, status=status)

    def download(self, request, *args, **kwargs):
        pass


class CollectionImportViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):
        api = galaxy_pulp.GalaxyImportsApi(pulp.get_client())
        response = api.get(prefix=settings.API_PATH_PREFIX, id=pk)
        return Response(response)

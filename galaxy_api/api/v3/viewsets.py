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
from django.conf import settings
import galaxy_pulp
from rest_framework.response import Response
from rest_framework import viewsets

from galaxy_api.common import pulp


class CollectionViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        api = galaxy_pulp.GalaxyCollectionsApi(pulp.get_client())
        response = api.list(prefix=settings.API_PATH_PREFIX, **request.query_params.dict())
        return Response(response)

    def retrieve(self, request, *args, **kwargs):
        api = galaxy_pulp.GalaxyCollectionsApi(pulp.get_client())
        response = api.get(
            prefix=settings.API_PATH_PREFIX,
            namespace=self.kwargs['namespace'],
            name=self.kwargs['name']
        )
        return Response(response)


class CollectionVersionViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        api = galaxy_pulp.GalaxyCollectionsApi(pulp.get_client())
        response = api.list_versions(
            prefix=settings.API_PATH_PREFIX,
            namespace=self.kwargs['namespace'],
            name=self.kwargs['name'],
            **request.query_params.dict()
        )
        return Response(response)

    def retrieve(self, request, *args, **kwargs):
        api = galaxy_pulp.GalaxyCollectionsApi(pulp.get_client())
        response = api.get_version(
            prefix=settings.API_PATH_PREFIX,
            namespace=self.kwargs['namespace'],
            name=self.kwargs['name'],
            version=self.kwargs['version'],
        )
        return Response(response)


class CollectionArtifactViewSet(viewsets.ViewSet):

    def upload(self, request, *args, **kwargs):
        pass

    def download(self, request, *args, **kwargs):
        pass

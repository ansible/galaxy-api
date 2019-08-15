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
from rest_framework import viewsets

from galaxy_api.pulp.galaxy import CollectionApi, CollectionVersionApi
from galaxy_api.pulp.galaxy import make_galaxy_client, make_response


class CollectionViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        api = CollectionApi(make_galaxy_client())
        response = api.list(params=request.query_params)
        return make_response(response)

    def retrieve(self, request, *args, **kwargs):
        api = CollectionApi(make_galaxy_client())
        response = api.read(self.kwargs['namespace'], self.kwargs['name'])
        return make_response(response)


class CollectionVersionViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        api = CollectionVersionApi(make_galaxy_client())
        response = api.list(
            namespace=self.kwargs['namespace'],
            name=self.kwargs['name'],
            params=request.query_params)
        return make_response(response)

    def retrieve(self, request, *args, **kwargs):
        api = CollectionVersionApi(make_galaxy_client())
        response = api.read(
            namespace=self.kwargs['namespace'],
            name=self.kwargs['name'],
            version=self.kwargs['version'])
        return make_response(response)


class CollectionArtifactViewSet(viewsets.ViewSet):

    def upload(self, request, *args, **kwargs):
        pass

    def download(self, request, *args, **kwargs):
        pass

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
"""Pulp Ansible API client."""

import urllib.parse as urlparse
import requests
from django.conf import settings
from django.http import HttpResponse
from requests.structures import CaseInsensitiveDict
from rest_framework.response import Response


class ApiClient:
    """Pulp Ansible Galaxy API v3 client."""

    prefix = 'pulp_ansible/galaxy/{_distro}/api/v3/'

    def __init__(self, host, port, pulp_distro):
        self.host = host
        self.port = port
        self.pulp_distro = pulp_distro

        self._base_url = 'http://{host}:{port}'.format(host=self.host, port=self.port)
        self._session = requests.Session()

    def call(self, method, path, *, path_params=None, query_params=None, headers=None):
        params = dict(path_params or {}, _distro=self.pulp_distro)
        url = self._make_url(path, params)

        headers = CaseInsensitiveDict(headers or {})
        headers.setdefault('Accept', 'application/json')

        return self._session.request(method, url, params=query_params, headers=headers)

    def _make_url(self, path, params):
        path = self.prefix + path
        params = {k: urlparse.quote(v) for k, v in params.items()}
        path = path.format(**params)
        return urlparse.urljoin(self._base_url, path)


class _BaseApi:
    """Base API client."""

    def __init__(self, api_client):
        self.api_client = api_client


class CollectionApi(_BaseApi):
    """Collection API client."""

    list_url = 'collections/'
    read_url = list_url + '{namespace}/{name}/'

    def list(self, *, params):
        return self.api_client.call(
            'GET',
            self.list_url,
            query_params=params)

    def read(self, namespace, name):
        path_params = {'namespace': namespace, 'name': name}
        return self.api_client.call('GET', self.read_url, path_params=path_params)


class CollectionVersionApi(_BaseApi):
    """Collection Versions API client."""

    list_url = 'collections/{namespace}/{name}/versions/'
    read_url = list_url + '{version}/'

    def list(self, namespace, name, *, params):
        path_params = {'namespace': namespace, 'name': name}
        return self.api_client.call(
            'GET',
            self.list_url,
            path_params=path_params,
            query_params=params)

    def read(self, namespace, name, version):
        path_params = {'namespace': namespace, 'name': name, 'version': version}
        return self.api_client.call('GET', self.read_url, path_params=path_params)


def make_galaxy_client():
    return ApiClient(
        host=settings.PULP_API_HOST,
        port=settings.PULP_API_PORT,
        pulp_distro=settings.PULP_DISTRIBUTION
    )


def make_response(response):
    # If response is JSON, return DRF response
    if response.content and response.headers['Content-Type'] == 'application/json':
        return Response(response.json(), status=response.status_code)
    # Otherwise return raw HttpResponse
    return HttpResponse(response.content, status=response.status_code)

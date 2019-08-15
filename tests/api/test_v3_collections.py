from unittest import mock

from django.conf import settings
from galaxy_api.auth.auth import RHEntitlementRequired
from rest_framework.response import Response
from rest_framework.test import APIClient

import pytest

from galaxy_api.auth.models import User


API_PREFIX = "/" + settings.API_PATH_PREFIX.strip("/")


class ProxyViewSetTest:
    @pytest.fixture(autouse=True)
    def rh_entitlement_patch(self):
        with mock.patch.object(RHEntitlementRequired, "has_permission", return_value=True):
            yield

    @pytest.fixture(autouse=True)
    def authenticate(self, api_client: APIClient):
        user = User(username="testuser")
        api_client.force_authenticate(user=user)

    @pytest.fixture()
    def make_response(self):
        with mock.patch("galaxy_api.api.v3.viewsets.make_response") as m:
            yield m


class TestCollectionViewSet(ProxyViewSetTest):
    @pytest.fixture()
    def collection_api(self):
        with mock.patch("galaxy_api.api.v3.viewsets.CollectionApi") as m:
            yield m.return_value

    def test_list(
        self, api_client: APIClient, collection_api: mock.Mock, make_response: mock.Mock
    ):
        make_response.return_value = Response()

        response = api_client.get(API_PREFIX + "/v3/collections/")

        assert response.status_code == 200
        collection_api.list.assert_called_once_with(params={})

    def test_list_limit_offset(
        self, api_client: APIClient, collection_api: mock.Mock, make_response: mock.Mock
    ):
        make_response.return_value = Response()

        response = api_client.get(
            API_PREFIX + "/v3/collections/", data={"limit": 10, "offset": 20}
        )

        assert response.status_code == 200
        collection_api.list.assert_called_once()
        params = collection_api.list.call_args[1]["params"]
        assert params["limit"] == "10"
        assert params["offset"] == "20"

    def test_retrieve(
        self, api_client: APIClient, collection_api: mock.Mock, make_response: mock.Mock
    ):
        make_response.return_value = Response()

        response = api_client.get(API_PREFIX + "/v3/collections/ansible/nginx/")

        assert response.status_code == 200
        collection_api.read.assert_called_once_with("ansible", "nginx")


class TestCollectionVersionViewSet(ProxyViewSetTest):
    @pytest.fixture()
    def version_api(self):
        with mock.patch("galaxy_api.api.v3.viewsets.CollectionVersionApi") as m:
            yield m.return_value

    def test_list(self, api_client: APIClient, version_api: mock.Mock, make_response: mock.Mock):
        make_response.return_value = Response()

        response = api_client.get(API_PREFIX + "/v3/collections/ansible/nginx/versions/")

        assert response.status_code == 200
        version_api.list.assert_called_once_with(namespace="ansible", name="nginx", params={})

    def test_list_limit_offset(
        self, api_client: APIClient, version_api: mock.Mock, make_response: mock.Mock
    ):
        make_response.return_value = Response()

        response = api_client.get(
            API_PREFIX + "/v3/collections/ansible/nginx/versions/",
            data={"limit": 10, "offset": 20},
        )

        assert response.status_code == 200
        version_api.list.assert_called_once_with(
            namespace="ansible", name="nginx", params=mock.ANY
        )
        params = version_api.list.call_args[1]["params"]
        assert params["limit"] == "10"
        assert params["offset"] == "20"

    def test_retrieve(
        self, api_client: APIClient, version_api: mock.Mock, make_response: mock.Mock
    ):
        make_response.return_value = Response()

        response = api_client.get(API_PREFIX + "/v3/collections/ansible/nginx/versions/1.2.3/")

        assert response.status_code == 200
        version_api.read.assert_called_once_with(
            namespace="ansible", name="nginx", version="1.2.3"
        )

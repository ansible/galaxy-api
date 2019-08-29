import unittest
from unittest import mock

import galaxy_pulp
from django.conf import settings
from rest_framework.test import APIClient

from galaxy_api.auth.auth import RHEntitlementRequired
from galaxy_api.auth.models import User

API_PREFIX = settings.API_PATH_PREFIX.strip("/")


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()

        user = User(username="testuser")
        self.client.force_authenticate(user=user)

        # Permission mock
        patcher = mock.patch.object(
            RHEntitlementRequired, "has_permission", return_value=True
        )
        patcher.start()
        self.addCleanup(patcher.stop)


class TestCollectionViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

        patcher = mock.patch("galaxy_pulp.GalaxyCollectionsApi")
        self.collection_api = patcher.start().return_value
        self.addCleanup(patcher.stop)

    def test_list(self):
        self.collection_api.list.return_value = galaxy_pulp.ResultsPage(
            count=1, results=[]
        )
        response = self.client.get(f"/{API_PREFIX}/v3/collections/")

        assert response.status_code == 200
        self.collection_api.list.assert_called_once_with(
            prefix=API_PREFIX, offset=0, limit=10
        )

    def test_list_limit_offset(self):
        self.collection_api.list.return_value = galaxy_pulp.ResultsPage(
            count=1, results=[]
        )
        response = self.client.get(
            f"/{API_PREFIX}/v3/collections/", data={"limit": 10, "offset": 20}
        )

        assert response.status_code == 200
        self.collection_api.list.assert_called_once_with(
            prefix=API_PREFIX, limit=10, offset=20
        )

    def test_retrieve(self):
        self.collection_api.get.return_value = {}
        response = self.client.get(f"/{API_PREFIX}/v3/collections/ansible/nginx/")

        assert response.status_code == 200
        self.collection_api.get.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx"
        )


class TestCollectionVersionViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

        patcher = mock.patch("galaxy_pulp.GalaxyCollectionsApi")
        self.collection_api = patcher.start().return_value
        self.addCleanup(patcher.stop)

    def test_list(self):
        self.collection_api.list_versions.return_value = galaxy_pulp.ResultsPage(
            count=1, results=[]
        )
        response = self.client.get(
            f"/{API_PREFIX}/v3/collections/ansible/nginx/versions/"
        )

        assert response.status_code == 200
        self.collection_api.list_versions.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx", limit=10, offset=0
        )

    def test_list_limit_offset(self):
        self.collection_api.list_versions.return_value = galaxy_pulp.ResultsPage(
            count=1, results=[]
        )
        response = self.client.get(
            f"/{API_PREFIX}/v3/collections/ansible/nginx/versions/",
            data={"limit": 10, "offset": 20},
        )

        assert response.status_code == 200
        self.collection_api.list_versions.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx", limit=10, offset=20
        )

    def test_retrieve(self):
        self.collection_api.get_version.return_value = {}
        response = self.client.get(
            f"/{API_PREFIX}/v3/collections/ansible/nginx/versions/1.2.3/"
        )

        assert response.status_code == 200
        self.collection_api.get_version.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx", version="1.2.3"
        )


class TestCollectionImportViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

        patcher = mock.patch("galaxy_pulp.GalaxyImportsApi")
        self.imports_api = patcher.start().return_value
        self.addCleanup(patcher.stop)

    def test_retrieve(self):
        self.imports_api.get.return_value = {}
        response = self.client.get(
            f"/{API_PREFIX}/v3/imports/collections/3e26b82c-702f-4bdd-a568-7d9db17759c1/"
        )

        assert response.status_code == 200
        self.imports_api.get.assert_called_once_with(
            prefix=API_PREFIX, id="3e26b82c-702f-4bdd-a568-7d9db17759c1"
        )

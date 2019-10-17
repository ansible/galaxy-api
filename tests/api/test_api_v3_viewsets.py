from unittest import mock

import galaxy_pulp

from .base import BaseTestCase, API_PREFIX


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

        patcher = mock.patch("galaxy_pulp.GalaxyCollectionVersionsApi", spec=True)
        self.versions_api = patcher.start().return_value
        self.addCleanup(patcher.stop)

    def test_list_empty(self):
        self.versions_api.list.return_value = galaxy_pulp.ResultsPage(
            count=1, results=[]
        )
        response = self.client.get(
            f"/{API_PREFIX}/v3/collections/ansible/nginx/versions/"
        )

        assert response.status_code == 404
        self.versions_api.list.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx", limit=10, offset=0
        )

    def test_list(self):
        self.versions_api.list.return_value = galaxy_pulp.ResultsPage(
            count=1, results=[{}]
        )
        response = self.client.get(
            f"/{API_PREFIX}/v3/collections/ansible/nginx/versions/"
        )

        assert response.status_code == 200
        self.versions_api.list.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx", limit=10, offset=0
        )

    def test_list_limit_offset(self):
        self.versions_api.list.return_value = galaxy_pulp.ResultsPage(
            count=1, results=[{}]
        )
        response = self.client.get(
            f"/{API_PREFIX}/v3/collections/ansible/nginx/versions/",
            data={"limit": 10, "offset": 20},
        )

        assert response.status_code == 200
        self.versions_api.list.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx", limit=10, offset=20
        )

    def test_list_limit_offset_empty(self):
        self.versions_api.list.return_value = galaxy_pulp.ResultsPage(
            count=1, results=[]
        )
        response = self.client.get(
            f"/{API_PREFIX}/v3/collections/ansible/nginx/versions/",
            data={"limit": 10, "offset": 20},
        )

        assert response.status_code == 404
        self.versions_api.list.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx", limit=10, offset=20
        )

    def test_retrieve(self):
        self.versions_api.get.return_value = {
            'namespace': 'ansible',
            'name': 'nginx',
            'version': '1.2.3',
            'download_url': '/v3/artifacts/collections/ansible-nginx-1.2.3.tar.gz',
        }
        response = self.client.get(
            f"/{API_PREFIX}/v3/collections/ansible/nginx/versions/1.2.3/"
        )

        assert response.status_code == 200
        assert response.data['download_url'] == \
            'http://testserver/v3/artifacts/collections/ansible-nginx-1.2.3.tar.gz'
        self.versions_api.get.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx", version="1.2.3"
        )


class TestCollectionImportViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

        patcher = mock.patch("galaxy_pulp.GalaxyImportsApi", spec=True)
        self.imports_api = patcher.start().return_value
        self.addCleanup(patcher.stop)

    def test_retrieve(self):
        self.imports_api.get.return_value = galaxy_pulp.CollectionImport()
        response = self.client.get(
            f"/{API_PREFIX}/v3/imports/collections/3e26b82c-702f-4bdd-a568-7d9db17759c1/"
        )

        assert response.status_code == 200
        self.imports_api.get.assert_called_once_with(
            prefix=API_PREFIX, id="3e26b82c-702f-4bdd-a568-7d9db17759c1"
        )

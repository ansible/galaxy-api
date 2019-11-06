from unittest import mock

from rest_framework.test import APIClient
import galaxy_pulp

from galaxy_api.auth import models as auth_models

from .base import BaseTestCase, API_PREFIX
from .x_rh_identity import user_x_rh_identity

import logging
log = logging.getLogger(__name__)


class TestCollectionViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

        patcher = mock.patch("galaxy_pulp.GalaxyCollectionsApi", spec=True)
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

    def test_update_for_namespace(self):
        username = 'some_namespace_member'
        some_namespace_member = auth_models.User.objects.create(username=username)
        namespace_group = self._create_group('rh-identity', 'some_namespace',
                                             users=some_namespace_member)
        namespace = self._create_namespace('some_namespace', namespace_group)
        log.debug('namespace: %s', namespace)

        some_namespace_member_token_b64 = user_x_rh_identity(username)

        client = APIClient()
        client.credentials(**{"HTTP_X_RH_IDENTITY": some_namespace_member_token_b64})

        self.collection_api.put.return_value = \
            galaxy_pulp.models.Collection(namespace='some_namespace',
                                          name='nginx',
                                          deprecated=False)

        response = client.put(f"/{API_PREFIX}/v3/collections/some_namespace/nginx/",
                              data={'namespace': 'some_namespace',
                                    'name': 'nginx',
                                    'foo': 'bar'},
                              format='json',
                              )

        assert response.status_code == 200

    def test_update_for_partner(self):
        partner_group = self._create_group('system', 'partner-engineers', users=self.user)
        namespace = self._create_namespace('test', partner_group)
        log.debug('namespace: %s', namespace)

        test_user_token_b64 = user_x_rh_identity('test')

        client = APIClient()
        client.credentials(**{"HTTP_X_RH_IDENTITY": test_user_token_b64})

        self.collection_api.put.return_value = \
            galaxy_pulp.models.Collection(namespace='test',
                                          name='nginx',
                                          deprecated=False)
        response = client.put(f"/{API_PREFIX}/v3/collections/test/nginx/",
                              data={'namespace': 'test',
                                    'name': 'nginx',
                                    'foo': 'bar'},
                              format='json')

        assert response.status_code == 200

    def test_update_for_non_namespace_member(self):
        username = 'some_namespace_member'
        not_username = 'not_namespace_member'
        some_namespace_member = auth_models.User.objects.create(username=username)
        not_namespace_member = auth_models.User.objects.create(username=not_username)

        namespace_group = self._create_group('rh-identity', 'some_namespace',
                                             users=some_namespace_member)
        namespace = self._create_namespace('some_namespace', namespace_group)
        log.debug('namespace: %s', namespace)

        bad_namespace_group = self._create_group('rh-identity', 'bad_namespace',
                                                 users=not_namespace_member)
        bad_namespace = self._create_namespace('bad_namespace', bad_namespace_group)
        log.debug('bad_namespace: %s', bad_namespace)

        not_namespace_member_token_b64 = user_x_rh_identity('not_namespace_member')

        # creds for a user in a different namespace
        client = APIClient()
        client.credentials(**{"HTTP_X_RH_IDENTITY": not_namespace_member_token_b64})

        self.collection_api.put.return_value = \
            galaxy_pulp.models.Collection(namespace='some_namespace',
                                          name='nginx',
                                          deprecated=False)

        # trying to modify collection in a different namespace
        response = client.put(f"/{API_PREFIX}/v3/collections/some_namespace/nginx/",
                              data={'namespace': 'some_namespace',
                                    'name': 'nginx',
                                    'foo': 'bar'},
                              format='json',
                              )

        response_data = response.json()

        assert response_data['errors'][0]['code'] == 'permission_denied'
        assert response_data['errors'][0]['status'] == '403'
        assert response.status_code == 403


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

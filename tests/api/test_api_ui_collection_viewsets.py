from unittest import mock

from .base import BaseTestCase, API_PREFIX


class TestCollectionVersionViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

        patcher = mock.patch("galaxy_pulp.GalaxyCollectionVersionsApi", spec=True)
        self.versions_api = patcher.start().return_value
        self.addCleanup(patcher.stop)

    def test_set_certified(self):
        self.versions_api.set_certified.return_value = {}

        response = self.client.put(
            f"/{API_PREFIX}/v3/_ui/collections/ansible/nginx/versions/1.2.3/certified/"
        )

        self.versions_api.set_certified.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx", version="1.2.3"
        )

        assert response.status_code == 200
        assert response.data == {}

    def test_unset_certified(self):
        self.versions_api.unset_certified.return_value = {}

        response = self.client.delete(
            f"/{API_PREFIX}/v3/_ui/collections/ansible/nginx/versions/1.2.3/certified/"
        )

        self.versions_api.unset_certified.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx", version="1.2.3"
        )

        assert response.status_code == 200
        assert response.data == {}

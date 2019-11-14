from unittest import mock

from galaxy_pulp.models import CertificationInfo

from .base import BaseTestCase, API_PREFIX


class TestCollectionVersionViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

        # NOTE: Should be in fixtures
        self.partner_group = self._create_group('system', 'partner-engineers', users=self.user)
        self.namespace = self._create_namespace('ansible', self.partner_group)

        patcher = mock.patch("galaxy_pulp.GalaxyCollectionVersionsApi", spec=True)
        self.versions_api = patcher.start().return_value
        self.addCleanup(patcher.stop)

    def test_set_certified(self):
        self.versions_api.set_certified.return_value = {}

        response = self.client.put(
            f"/{API_PREFIX}/v3/_ui/collection-versions/ansible/nginx/1.2.3/certified/",
            data={'certification': 'certified'},
            format='json',
        )

        assert response.status_code == 200
        assert response.data == {}
        self.versions_api.set_certified.assert_called_once_with(
            prefix=API_PREFIX, namespace="ansible", name="nginx",
            version="1.2.3", certification_info=CertificationInfo('certified')
        )

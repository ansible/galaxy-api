from unittest import mock

from .base import BaseTestCase


class TestCollectionVersionViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

        # NOTE: Should be in fixtures
        self.partner_group = self._create_group('system', 'partner-engineers', users=self.user)
        self.namespace = self._create_namespace('ansible', self.partner_group)

        patcher = mock.patch("galaxy_pulp.GalaxyCollectionVersionsApi", spec=True)
        self.versions_api = patcher.start().return_value
        self.addCleanup(patcher.stop)

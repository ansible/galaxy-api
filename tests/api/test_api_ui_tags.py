from unittest import mock

import galaxy_pulp

from .base import BaseTestCase, API_PREFIX


class TestTagsViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

        patcher = mock.patch("galaxy_pulp.PulpTagsApi", spec=True)
        self.tags_api = patcher.start().return_value
        self.addCleanup(patcher.stop)

    def test_list(self):
        self.tags_api.list.return_value = galaxy_pulp.ResultsPage(
            count=2, results=[{"name": "foo"}, {"name": "bar"}]
        )
        response = self.client.get(f"/{API_PREFIX}/v3/_ui/tags/")

        self.tags_api.list.assert_called_once_with(offset=0, limit=10)
        assert response.status_code == 200
        assert response.data['meta']['count'] == 2
        assert response.data['data'] == [{"name": "foo"}, {"name": "bar"}]

    def test_list_limit_offset(self):
        self.tags_api.list.return_value = galaxy_pulp.ResultsPage(
            count=0, results=[]
        )
        response = self.client.get(
            f"/{API_PREFIX}/v3/_ui/tags/", data={"limit": 10, "offset": 20}
        )

        assert response.status_code == 200
        self.tags_api.list.assert_called_once_with(limit=10, offset=20)

from .base import BaseTestCase, API_PREFIX


class TestApiRootView(BaseTestCase):
    def test_get(self):
        response = self.client.get(f"/{API_PREFIX}/")

        assert response.status_code == 200
        assert response.data == {
            "available_versions": {"v3": "v3/"},
        }

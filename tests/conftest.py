import pytest
from rest_framework import test as drf_test


@pytest.fixture()
def api_client():
    return drf_test.APIClient()

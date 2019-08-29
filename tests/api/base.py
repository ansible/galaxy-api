import unittest
from unittest import mock

from django.conf import settings
from rest_framework.test import APIClient

from galaxy_api.auth.auth import RHEntitlementRequired
from galaxy_api.auth.models import User


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


API_PREFIX = settings.API_PATH_PREFIX.strip("/")

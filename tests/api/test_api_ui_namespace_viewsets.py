import logging

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from galaxy_api.auth import models as auth_models

from .base import BaseTestCase
from .x_rh_identity import user_x_rh_identity


log = logging.getLogger(__name__)


class TestUiNamespaceViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_get(self):
        url = reverse('api:ui:namespaces-list')
        response = self.client.get(url, format='json')

        log.debug('response: %s', response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_new_user(self):
        username = 'newuser'
        username_token_b64 = user_x_rh_identity(username,
                                                account_number="666")

        client = APIClient()
        client.credentials(**{"HTTP_X_RH_IDENTITY": username_token_b64})

        url = reverse('api:ui:namespaces-list')

        response = client.get(url, format='json')

        log.debug('response: %s', response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user isn't a namespace owner, should get empty list of namespaces
        assert not response.data['data']

    def test_get_namespace_owner_user(self):
        username = 'some_namespace_member'
        some_namespace_member = auth_models.User.objects.create(username=username)
        namespace_group = self._create_group('rh-identity', 'some_namespace',
                                             users=some_namespace_member)
        namespace = self._create_namespace('some_namespace', namespace_group)
        log.debug('namespace: %s', namespace)

        some_namespace_member_token_b64 = user_x_rh_identity(username)

        client = APIClient()
        client.credentials(**{"HTTP_X_RH_IDENTITY": some_namespace_member_token_b64})

        url = reverse('api:ui:namespaces-list')

        response = client.get(url, format='json')

        log.debug('response: %s', response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['name'], 'some_namespace')

    # TODO: test get detail, put/update detail, put/update detail for partner-engineers, etc

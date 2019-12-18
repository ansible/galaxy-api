import json
import logging

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from galaxy_api.api import models
from galaxy_api.auth import models as auth_models
from galaxy_api.api import permissions

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

    def test_post_namespace(self):
        username = 'saruman'
        username_token_b64 = user_x_rh_identity(username, account_number="999")
        some_namespace_member = auth_models.User.objects.create(username=username)
        client = APIClient()
        client.credentials(**{"HTTP_X_RH_IDENTITY": username_token_b64})

        namespace_group_name = permissions.IsPartnerEngineer.GROUP_NAME
        namespace_group = auth_models.Group.objects.create(name=namespace_group_name)
        namespace_group.user_set.add(*[some_namespace_member])

        url = reverse('api:ui:namespaces-list')
        payload = {'name': 'mordor',
                   'company': 'coolring',
                   'email': 'saru@man.me',
                   'description': 'isengard',
                   'groups': ['system:partner-engineers']}

        response = client.post(url, format='json', data=payload)
        log.debug('%s', response.content)
        log.debug('%s', response.status_code)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_namespace(self):
        username = 'saruman'
        username_token_b64 = user_x_rh_identity(username, account_number="999")
        some_namespace_member = auth_models.User.objects.create(username=username)
        client = APIClient()
        client.credentials(**{"HTTP_X_RH_IDENTITY": username_token_b64})

        namespace_group_name = permissions.IsPartnerEngineer.GROUP_NAME
        namespace_group = auth_models.Group.objects.create(name=namespace_group_name)
        namespace_group.user_set.add(*[some_namespace_member])

        # create
        url = reverse('api:ui:namespaces-list')
        payload = {'name': 'mordor',
                   'company': 'coolring',
                   'email': 'saru@man.me',
                   'description': 'isengard',
                   'groups': ['system:partner-engineers']}
        client.post(url, format='json', data=payload)

        # update
        url += 'mordor/'
        log.debug('%s', url)
        payload = {'name': 'mandarin',
                   'email': 'saru@man.me',
                   'description': 'lemonade',
                   'groups': ['system:partner-engineers']}

        response = client.put(url, format='json', data=payload)
        response_data = json.loads(response.content.decode('utf-8'))
        log.debug('%s', response.content)
        log.debug('%s', response.status_code)

        self.assertEqual(response_data['name'], 'mordor')
        self.assertEqual(response_data['description'], 'lemonade')
        self.assertEqual(response_data['company'], 'coolring')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO: test get detail, put/update detail, put/update detail for partner-engineers, etc


class TestUiMyNamespaceViewSet(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_list_user_not_in_namespace_group(self):
        url = reverse('api:ui:namespaces-list')
        username = 'not_namespace_member'

        not_namespace_member_token_b64 = user_x_rh_identity(username)

        client = APIClient()
        client.credentials(**{"HTTP_X_RH_IDENTITY": not_namespace_member_token_b64})

        response = client.get(url, format='json')

        log.debug('response: %s', response)
        log.debug('response.data:\n%s', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # No matching namespaces found
        self.assertEqual(response.data['data'], [])

    def test_list_user_in_namespace_group(self):
        url = reverse('api:ui:namespaces-list')

        username = 'some_namespace_member'
        some_namespace_member = auth_models.User.objects.create(username=username)

        namespace_group = self._create_group('rh-identity', 'some_namespace',
                                             users=some_namespace_member)
        namespace = self._create_namespace('some_namespace', namespace_group)

        log.debug('namespace: %s', namespace)

        some_namespace_member_token_b64 = user_x_rh_identity(username)

        client = APIClient()
        client.credentials(**{"HTTP_X_RH_IDENTITY": some_namespace_member_token_b64})

        response = client.get(url, format='json')

        log.debug('response: %s', response)
        log.debug('response.data:\n%s', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['name'], 'some_namespace')

    def test_list_user_in_namespace_system_admin(self):
        url = reverse('api:ui:namespaces-list')

        username = 'some_namespace_member'
        some_namespace_member = auth_models.User.objects.create(username=username)

        namespace_group_name = permissions.IsPartnerEngineer.GROUP_NAME
        namespace_group = auth_models.Group.objects.create(name=namespace_group_name)
        namespace_group.user_set.add(*[some_namespace_member])

        namespace = self._create_namespace('some_namespace', namespace_group)

        # create another namespace without any groups
        another_namespace = models.Namespace.objects.create(name='another_namespace')

        log.debug('namespace: %s', namespace)
        log.debug('another_namespace: %s', another_namespace)

        some_namespace_member_token_b64 = user_x_rh_identity(username)

        client = APIClient()
        client.credentials(**{"HTTP_X_RH_IDENTITY": some_namespace_member_token_b64})

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['name'], 'some_namespace')
        namespace_names = [ns_data['name'] for ns_data in response.data['data']]

        # Verify the system user can see all namespacees, even those without a group
        self.assertIn('some_namespace', namespace_names)
        self.assertIn('another_namespace', namespace_names)

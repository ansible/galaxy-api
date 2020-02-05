from django.contrib.auth import models as auth_models

from django_prometheus.models import ExportModelOperationsMixin

__all__ = (
    'SYSTEM_SCOPE',
    'User',
    'Group',
)


SYSTEM_SCOPE = 'system'


class User(ExportModelOperationsMixin('user'), auth_models.AbstractUser):
    """Custom user model."""
    pass


class GroupManager(ExportModelOperationsMixin('groupmanager'), auth_models.GroupManager):
    def create_identity(self, scope, name):
        return super().create(name=self._make_name(scope, name))

    def get_or_create_identity(self, scope, name):
        return super().get_or_create(name=self._make_name(scope, name))

    @staticmethod
    def _make_name(scope, name):
        return f'{scope}:{name}'


class Group(ExportModelOperationsMixin('group'), auth_models.Group):
    objects = GroupManager()

    class Meta:
        proxy = True

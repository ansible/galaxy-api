from django.db import models
from django.contrib.auth.models import AbstractUser

from galaxy_api.common import models as common_models


__all__ = (
    'User',
    'Tenant',
)


class User(AbstractUser):
    """Custom user model."""
    pass


class Tenant(common_models.TimestampsMixin):
    """
    Model representing tenant concept.

    Tenant is a special model that usually represents user or
    group (organization). It allows configuring objects permissions
    or ownership more flexibly.

    Fields:
        name: Tenant name.

    Relations:
        users: Many to many relationship with users.
    """

    name = models.CharField(max_length=150, unique=True)
    users = models.ManyToManyField(User, related_name='tenants')

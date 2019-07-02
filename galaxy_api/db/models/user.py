from django.conf import settings
from django.db import models


__all__ = (
    'UserProfile',
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

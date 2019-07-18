from django.db import models


__all__ = (
    'TimestampsMixin',
)


class TimestampsMixin(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

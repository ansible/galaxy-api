"""URLs Configuration."""

from django.conf import settings
from django.urls import include, path


api_prefix = settings.API_PATH_PREFIX.strip('/')
urlpatterns = [
    path(f'{api_prefix}/', include('galaxy_api.api.urls', namespace='api')),
]

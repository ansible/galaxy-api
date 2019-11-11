"""URLs Configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


api_prefix = settings.API_PATH_PREFIX.strip('/')
urlpatterns = [
    path(f'{api_prefix}/', include('galaxy_api.api.urls', namespace='api')),

    path('admin/', admin.site.urls),
]

if settings.STATIC_ROOT:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

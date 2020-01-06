"""URLs Configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve as serve_static


api_prefix = settings.API_PATH_PREFIX.strip('/')
urlpatterns = [
    path(f'{api_prefix}/', include('galaxy_api.api.urls', namespace='api')),

    path('admin/', admin.site.urls),

    # provides /metrics for prometheus
    path('', include('django_prometheus.urls')),
]

# Serve static files for admin site
if not settings.DEBUG and settings.STATIC_ROOT:
    urlpatterns += [
        path(
            '{prefix}<path:path>'.format(prefix=settings.STATIC_URL.lstrip('/')),
            serve_static,
            kwargs={'document_root': settings.STATIC_ROOT},
        )
    ]

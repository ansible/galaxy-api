"""WSGI config."""

import os

from django.core.wsgi import get_wsgi_application

# Store prometheus stats based on uwsgi.worker_id instead of
# the default pid, since wsgi may create a lot of short lived pids
try:
    import prometheus_client
    import uwsgi
    prometheus_client.values.ValueClass = prometheus_client.values.MultiProcessValue(
        _pidFunc=uwsgi.worker_id)
except ImportError:
    pass  # not running in uwsgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'galaxy_api.settings')

application = get_wsgi_application()

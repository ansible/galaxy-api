"""API URLs Configuration."""

from django.urls import include, path

from .v3 import urls as urls_v3


app_name = 'api'
urlpatterns = [
    path('v3/', include(urls_v3, namespace='v3')),
]

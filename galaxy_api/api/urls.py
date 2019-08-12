"""API URLs Configuration."""

from django.urls import include, path

from .ui import urls as ui_urls


app_name = 'api'
urlpatterns = [
    path('v3/_ui/', include(ui_urls, namespace='ui')),
]

"""API URLs Configuration."""

from django.urls import include, path

from . import views
from .ui import urls as ui_urls
from .v3 import urls as v3_urls

app_name = "api"
urlpatterns = [
    path("", views.ApiRootView.as_view(), name="root"),
    path("v3/", include(v3_urls, namespace="v3"), name="v3_root"),
    path("v3/_ui/", include(ui_urls, namespace="ui")),
]

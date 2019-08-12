from django.urls import path, include
from rest_framework import routers

from . import viewsets


router = routers.SimpleRouter()
router.register('namespaces', viewsets.NamespaceViewSet)


app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]

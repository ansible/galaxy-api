from rest_framework import exceptions as exc
from rest_framework.response import Response
from rest_framework import status as http_codes
from rest_framework.views import APIView

from galaxy_common import models
from galaxy_api import tasks


__all__ = (
    'PingView'
)


class PingView(APIView):
    def get(self, request):
        ping = models.Ping.objects.first()
        if ping is None:
            raise exc.NotFound()
        return Response(ping.updated_at.isoformat())

    def post(self, request):
        tasks.ping()
        return Response(status=http_codes.HTTP_202_ACCEPTED)

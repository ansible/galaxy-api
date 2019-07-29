from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


__all__ = (
    'TestView'
)


class TestView(APIView):
    def get(self, request):
        return Response({
            '_href': reverse('api:v1:test'),
            'status': 'OK',
        })

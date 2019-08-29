from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse


class ApiRootView(views.APIView):
    def get(self, request):
        root_url = reverse("api:root")
        data = {
            "available_versions": {"v3": f"{root_url}v3/"},
        }
        return Response(data)

from rest_framework.views import APIView

from middleware.response import success

class HealthCheckView(APIView):
    def get(self, request):
        return success({}, "Heath check successful - django v3", True)
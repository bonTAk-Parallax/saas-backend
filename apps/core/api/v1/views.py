import redis
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connections
from django_redis import get_redis_connection

class HealthCheckView(APIView):
    permission_classes = []

    def get(self, request):
        status = {"status": "healthy", "database": "ok", "redis": "ok"}
        try:
            connections['default'].ensure_connection()
        except Exception:
            status["database"] = "error"
            status["status"] = "unhealthy"
        try:
            redis_client = redis.from_url(settings.REDIS_URL)
            redis_client.ping()
        except Exception:
            status["redis"] = "error"
            status["status"] = "unhealthy"
        return Response(status)
    
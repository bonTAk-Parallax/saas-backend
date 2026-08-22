import redis
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connections
from django_redis import get_redis_connection
from django.db.migrations.executor import MigrationExecutor

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

class ReadinessView(APIView):
    permission_classes = []

    def get(self, request):
        checks = {"migrations": "ok"}
        ready = True

        try:
            executor = MigrationExecutor(connections['default'])
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            if plan:
                checks["migrations"] = "pending"
                ready = False
        except Exception:
            checks["migrations"] = "error"
            ready = False

        return Response(
            {"status": "ready" if ready else "not_ready", "checks": checks},
            status=status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    
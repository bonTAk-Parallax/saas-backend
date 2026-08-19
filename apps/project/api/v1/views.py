
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_rq import enqueue
from apps.core.commons.mixins import TenantAwareMixin
from apps.core.models import ExportJob
from apps.core.permissions.permissions import HasTenantAccess, HasScope
from apps.project.models import Project
from apps.core.api.v1.serializers.export import ExportJobSerializer
from apps.project.api.v1.serializers import ProjectSerializer

class ProjectViewSet(TenantAwareMixin, viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related("tasks")
    serializer_class = ProjectSerializer

    permission_classes = [
        IsAuthenticated,
        HasTenantAccess,
        HasScope,
    ]

    required_scopes = {
        "list": {"projects:read"},
        "retrieve": {"projects:read"},
        "create": {"projects:write"},
        "update": {"projects:write"},
        "partial_update": {"projects:write"},
        "destroy": {"projects:delete"},
        "export": {"exports:create"},
    }

    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.profile.organization,
            created_by=self.request.user,
        )

    @action(detail=False, methods=["post"], url_path="export")
    def export(self, request):
        org = request.user.profile.organization

        job = enqueue(
            "apps.projects.tasks.generate_export",
            org.id,
        )

        export_job = ExportJob.objects.create(
            organization=org,
            job_id=job.id,
            status="PENDING",
        )

        return Response({"job_id": export_job.id})
    
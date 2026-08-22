
from apps.project.models import Project
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.core.commons.mixins import TenantAwareMixin
from apps.core.permissions.permissions import HasTenantAccess, HasScope
from apps.project.api.v1.serializers import ProjectSerializer
from apps.project.services.export import create_export_job, create_project

class ProjectViewSet(TenantAwareMixin, viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related("tasks")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, HasTenantAccess, HasScope]
    required_scopes = {
        "list": {"projects:read"}, "retrieve": {"projects:read"},
        "create": {"projects:write"}, "update": {"projects:write"},
        "partial_update": {"projects:write"}, "destroy": {"projects:delete"},
        "export": {"exports:create"},
    }

    def perform_create(self, serializer):
        project = create_project(
            organization=self.request.user.profile.organization,
            user=self.request.user,
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description', ''),
        )
        serializer.instance = project  

    # @action(detail=False, methods=["post"], url_path="export")
    # def export(self, request):
    #     export_job = create_export_job(
    #         organization=request.user.profile.organization, user=request.user,
    #     )
    #     return Response({"job_id": export_job.id}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="export")
    def export(self, request):
        export_job = create_export_job(
            organization=request.user.profile.organization, user=request.user,
        )
        # Reuse the real serializer instead of a hand-rolled dict, so the
        # create response and the later GET /export-jobs/{id}/ response
        # always agree on field names — no more silent "job_id" vs "id" drift.
        from apps.core.api.v1.serializers.export import ExportJobSerializer
        return Response(ExportJobSerializer(export_job).data, status=status.HTTP_201_CREATED)

    

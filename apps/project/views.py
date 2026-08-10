
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_rq import enqueue
from apps.core.commons.mixins import TenantAwareMixin
from apps.core.models import ExportJob
from apps.project.models import Project
from apps.core.serializers.export import ExportJobSerializer
from apps.project.serializers import ProjectSerializer
from apps.user.permissions import IsOrgMember

class ProjectViewSet(TenantAwareMixin, viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('tasks')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOrgMember]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='export')
    def export(self, request):
        org = request.user.profile.organization
        job = enqueue('apps.projects.tasks.generate_export', org.id)
        export_job = ExportJob.objects.create(
            organization=org,
            job_id=job.id,
            status='PENDING'
        )
        return Response({"job_id": export_job.id})
    
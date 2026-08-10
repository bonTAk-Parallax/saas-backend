
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.core.commons.mixins import TenantAwareMixin
from apps.task.models import Task, Comment
from apps.task.serializers.comments import CommentSerializer
from apps.task.serializers.tasks import TaskSerializer
from apps.user.permissions import IsOrgMember
from django.core.exceptions import PermissionDenied

class TaskViewSet(TenantAwareMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related('project', 'assigned_to')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOrgMember]

    def get_queryset(self):
        qs = super().get_queryset()
        project_id = self.request.query_params.get('project')
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if project.organization != self.request.user.profile.organization:
            raise PermissionDenied("Project does not belong to your organization.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, pk=None):
        task = self.get_object()
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(task=task, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        comments = task.comments.all().select_related('author')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
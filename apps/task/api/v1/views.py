
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.core.commons.mixins import TenantAwareMixin
from apps.task.models import Task, Comment
from apps.core.permissions.permissions import HasTenantAccess, HasScope
from apps.task.api.v1.serializers.comments import CommentSerializer
from apps.task.api.v1.serializers.tasks import TaskSerializer
from django.core.exceptions import PermissionDenied

class TaskViewSet(TenantAwareMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related(
        "project",
        "assigned_to",
    )
    serializer_class = TaskSerializer

    permission_classes = [
        IsAuthenticated,
        HasTenantAccess,
        HasScope,
    ]

    required_scopes = {
        "list": {"tasks:read"},
        "retrieve": {"tasks:read"},
        "create": {"tasks:write"},
        "update": {"tasks:write"},
        "partial_update": {"tasks:write"},
        "destroy": {"tasks:delete"},
        "comments": {"comments:read"},
    }

    def get_queryset(self):
        qs = super().get_queryset()

        project_id = self.request.query_params.get("project")

        if project_id:
            qs = qs.filter(project_id=project_id)

        return qs

    @action(detail=True, methods=["get", "post"], url_path="comments")
    def comments(self, request, pk=None):
        task = self.get_object()

        if request.method == "POST":
            serializer = CommentSerializer(
                data=request.data,
                context=self.get_serializer_context(),
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(
                task=task,
                author=request.user,
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        comments = task.comments.all().select_related("author")
        serializer = CommentSerializer(
            comments,
            many=True,
            context=self.get_serializer_context(),
        )

        return Response(serializer.data)
    
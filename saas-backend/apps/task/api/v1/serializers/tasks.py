
from datetime import timezone
from rest_framework import serializers
from apps.core.commons.dynamic_serializers import TenantAwareModelSerializer
from apps.task.models import Task

class TaskSerializer(TenantAwareModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'project_title', 
                  'assigned_to', 'assigned_to_username', 'is_done', 'due_date',
                  'created_at', 'updated_at', 'comments_count']
        read_only_fields = ['created_at', 'updated_at', 'comments_count']

    def validate_project(self, project):
        request = self.context['request']
        if project.organization_id != request.user.profile.organization_id:
            raise serializers.ValidationError("Project does not belong to your organization.")
        return project

    def validate_assigned_to(self, user):
        if user is None:
            return user
        request = self.context['request']
        if not hasattr(user, 'profile') or user.profile.organization_id != request.user.profile.organization_id:
            raise serializers.ValidationError("Cannot assign a task to a user outside your organization.")
        return user

    def validate_due_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


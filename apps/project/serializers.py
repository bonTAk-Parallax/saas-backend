
# apps/projects/serializers.py
from rest_framework import serializers
from apps.core.commons.dynamic_serializers import TenantAwareModelSerializer
from apps.project.models import Project

class ProjectSerializer(TenantAwareModelSerializer):
    task_count = serializers.IntegerField(source='tasks.count', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_by', 'created_by_username', 
                  'organization', 'created_at', 'updated_at', 'task_count']
        read_only_fields = ['created_by', 'organization', 'created_at', 'updated_at', 'task_count']


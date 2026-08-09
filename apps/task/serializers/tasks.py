
from rest_framework import serializers
from apps.core.commons.dynamic_serializers import DynamicFieldsModelSerializer
from apps.task.models import Task

class TaskSerializer(DynamicFieldsModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'project_title', 
                  'assigned_to', 'assigned_to_username', 'is_done', 'due_date',
                  'created_at', 'updated_at', 'comments_count']
        read_only_fields = ['created_at', 'updated_at', 'comments_count']

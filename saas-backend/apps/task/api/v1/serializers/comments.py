

from rest_framework import serializers
from apps.core.commons.dynamic_serializers import TenantAwareModelSerializer
from apps.task.models import Comment

class CommentSerializer(TenantAwareModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'author_username', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']


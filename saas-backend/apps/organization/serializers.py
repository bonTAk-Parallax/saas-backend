

from django.core import serializers
from .models import Invite

class InviteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ['id', 'email', 'role', 'token', 'expires_at']
        read_only_fields = ['id', 'token', 'expires_at']
 
    def create(self, validated_data):
        request = self.context['request']
        return Invite.objects.create(
            organization=request.user.profile.organization,
            invited_by=request.user,
            **validated_data,
        )
    

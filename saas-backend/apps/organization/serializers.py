

from datetime import timedelta
import secrets
from time import timezone

from django.db import transaction
from rest_framework import serializers
from .models import Invite
from apps.user.models import UserProfile

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
    

class BulkInviteCreateSerializer(serializers.Serializer):
    emails = serializers.ListField(
        child=serializers.EmailField(), min_length=1, max_length=50
    )
    role = serializers.CharField()
 
    def validate_role(self, value):
        if value not in {"ADMIN", "MANAGER", "MEMBER"}:
            raise serializers.ValidationError("Invalid role.")
        return value
 
    def create(self, validated_data):
        request = self.context['request']
        org = request.user.profile.organization
        role = validated_data['role']
        created, skipped = [], []
 
        with transaction.atomic():
            for raw_email in validated_data['emails']:
                email = raw_email.lower()
 
                if UserProfile.objects.filter(user__email__iexact=email, organization=org).exists():
                    skipped.append({"email": email, "reason": "already a member"})
                    continue
 
                existing = Invite.objects.filter(
                    organization=org, email=email, accepted_at__isnull=True
                ).first()
 
                if existing:
                    existing.role = role
                    existing.token = secrets.token_urlsafe(32)
                    existing.expires_at = timezone.now() + timedelta(days=7)
                    existing.invited_by = request.user
                    existing.save()
                    created.append(existing)
                else:
                    created.append(Invite.objects.create(
                        organization=org, email=email, role=role,
                        invited_by=request.user, token=secrets.token_urlsafe(32),
                        expires_at=timezone.now() + timedelta(days=7),
                    ))
 
        return {"created": created, "skipped": skipped}
    

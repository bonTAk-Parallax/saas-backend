import secrets
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.conf import settings
from apps.core.models.base import TenantScopedModel


class Organization(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def generate_invite_token():
    return secrets.token_urlsafe(32)

def default_invite_expiry():
    return timezone.now() + timedelta(days=7)
 
class Invite(TenantScopedModel):  
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="invites"
    )
    email = models.EmailField()
    role = models.CharField(max_length=20)  
    token = models.CharField(max_length=64, unique=True, default=generate_invite_token)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="invites_sent"
    )
    expires_at = models.DateTimeField(default=default_invite_expiry)
    accepted_at = models.DateTimeField(null=True, blank=True)
 
    TENANT_LOOKUP = "organization"
 
    class Meta:
        indexes = [models.Index(fields=["token"])]


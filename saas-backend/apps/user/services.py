
from django.db import transaction
from django.utils import timezone
from apps.organization.models import Organization
from apps.user.models import UserProfile
from django.contrib.auth import get_user_model
from rest_framework import serializers as drf_serializers
from apps.organization.models import Invite

User = get_user_model()

def register_user(*, username, email, password, organization_name):
    with transaction.atomic():
        user = User.objects.create_user(username=username, email=email, password=password)
        org = Organization.objects.create(name=organization_name)
        UserProfile.objects.create(user=user, organization=org, role='ADMIN')
    return user

 
def register_user_via_invite(*, username, email, password, invite_token):
    with transaction.atomic():
        try:
            invite = Invite.objects.select_for_update().get(
                token=invite_token, accepted_at__isnull=True
            )
        except Invite.DoesNotExist:
            raise drf_serializers.ValidationError(
                {"invite_token": "This invite is invalid or has already been used."}
            )
 
        if invite.expires_at < timezone.now():
            raise drf_serializers.ValidationError({"invite_token": "This invite has expired."})
 
        if invite.email.lower() != email.lower():
            raise drf_serializers.ValidationError(
                {"email": "This invite was issued for a different email address."}
            )
 
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, organization=invite.organization, role=invite.role)
 
        invite.accepted_at = timezone.now()
        invite.save(update_fields=["accepted_at"])
 
        return user



from django.db import transaction
from apps.organization.models import Organization
from apps.user.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

def register_user(*, username, email, password, organization_name):
    with transaction.atomic():
        user = User.objects.create_user(username=username, email=email, password=password)
        org = Organization.objects.create(name=organization_name)
        UserProfile.objects.create(user=user, organization=org, role='ADMIN')
    return user

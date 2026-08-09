from django.db import models
from django.conf import settings
from apps.organization.models import Organization


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="members",
    )

    role = models.CharField(max_length=20, default='MEMBER')
    last_activity = models.DateTimeField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
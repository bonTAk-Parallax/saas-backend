from django.db import models
from django.conf import settings
from apps.core.models.base import AuditModel, TenantScopedModel
from apps.organization.models import Organization


class Project(TenantScopedModel, AuditModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    TENANT_LOOKUP = "organization"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization', 'title'], name='unique_project_title_per_org')
        ]

    def __str__(self):
        return self.title
    
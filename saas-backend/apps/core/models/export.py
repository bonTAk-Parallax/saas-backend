from django.db import models

# from apps.core.models import BaseModel
from apps.core.models.base import TenantScopedModel
from apps.organization.models import Organization


class ExportJob(TenantScopedModel):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="export_jobs",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    file_url = models.CharField(
        max_length=500,
        blank=True,
    )

    job_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    TENANT_LOOKUP = 'organization'

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'status', 'created_at']),
        ]
    
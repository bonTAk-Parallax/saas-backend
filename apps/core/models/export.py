from django.db import models

from apps.core.models import BaseModel
from apps.organization.models import Organization


class ExportJob(BaseModel):

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
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    
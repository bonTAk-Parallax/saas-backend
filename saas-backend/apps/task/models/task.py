from django.db import models
from django.conf import settings
from apps.core.models.base import AuditModel, TenantScopedModel
from apps.project.models import Project


class Task(TenantScopedModel, AuditModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    is_done = models.BooleanField(default=False)
    due_date = models.DateField(
        null=True,
        blank=True,
    )

    TENANT_LOOKUP = "project__organization"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project', 'title'], name='unique_task_title_per_project')
        ]
        indexes = [
            models.Index(fields=['project', 'is_done']),
            models.Index(fields=['project', 'due_date']),
            models.Index(fields=['assigned_to']),
        ]


    def __str__(self):
        return self.title
    
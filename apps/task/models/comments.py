from django.db import models
from django.conf import settings
from apps.core.models.base import AuditModel, TenantScopedModel
from apps.task.models import Task


class Comment(TenantScopedModel, AuditModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField()

    TENANT_FIELD = "task__project__organization"

    def __str__(self):
        return f"{self.author} - {self.task}"
    
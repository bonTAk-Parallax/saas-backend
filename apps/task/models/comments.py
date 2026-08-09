from django.db import models
from django.conf import settings
from apps.core.models.base import AuditModel
from apps.task.models import Task


class Comment(AuditModel):
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

    def __str__(self):
        return f"{self.author} - {self.task}"
    
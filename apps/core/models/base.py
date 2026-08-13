
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(
            update_fields=["deleted_at", "updated_at"],
            using=using,
        )

    class Meta:
        abstract = True


class AuditModel(BaseModel):

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )

    class Meta:
        abstract = True


class TenantScopedModel(BaseModel):
    TENANT_LOOKUP: str = None

    class Meta:
        abstract = True

    @classmethod
    def tenant_lookup(cls, organization):
        if cls.TENANT_LOOKUP is None:
            raise NotImplementedError(f"{cls.__name__} must define TENANT_LOOKUP")
        return {cls.TENANT_LOOKUP: organization}

    @classmethod
    def is_root_tenant_field(cls):
        """True if this model's tenant lookup IS the organization FK directly
        (e.g. Project.organization), vs. reached through a chain (e.g. Task.project__organization)."""
        return cls.TENANT_LOOKUP is not None and "__" not in cls.TENANT_LOOKUP

    def resolve_tenant(self):
        value = self
        for part in self.TENANT_LOOKUP.split("__"):
            value = getattr(value, part)
        return value
    
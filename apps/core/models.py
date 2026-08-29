"""
Core base models with UUIDs, timestamps, and soft deletion.
"""
import uuid
from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    """Abstract base model with created_at and updated_at timestamps."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class TenantScopedModel(TimeStampedModel):
    """Abstract model enforcing multi-tenant workspace isolation."""
    workspace = models.ForeignKey(
        'workspaces.Workspace',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_set",
        db_index=True
    )

    class Meta:
        abstract = True

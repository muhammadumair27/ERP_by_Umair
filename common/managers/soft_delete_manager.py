"""Default manager for soft-delete aware models."""

from django.db import models

from common.querysets.soft_delete_queryset import SoftDeleteQuerySet


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """Hide soft-deleted rows from ordinary queries."""

    def get_queryset(self):
        """Return the default queryset without soft-deleted rows."""

        return super().get_queryset().filter(is_deleted=False)

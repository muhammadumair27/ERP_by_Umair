"""Manager that includes soft-deleted rows."""

from django.db import models

from common.querysets.soft_delete_queryset import SoftDeleteQuerySet


class AllObjectsManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """Expose every row, including the soft-deleted ones."""

    def get_queryset(self):
        """Return the default queryset without filtering."""

        return super().get_queryset()

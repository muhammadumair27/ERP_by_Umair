"""QuerySet with soft-delete aware bulk operations."""

from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """Support soft deletion, restoration and filtering in bulk."""

    def delete(self):
        """Soft-delete every row in the queryset."""

        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently remove every row in the queryset."""

        return super().delete()

    def alive(self):
        """Return only the rows that have not been deleted."""

        return self.filter(is_deleted=False)

    def dead(self):
        """Return only the rows that have been soft-deleted."""

        return self.filter(is_deleted=True)

    def restore(self):
        """Bring every soft-deleted row in the queryset back."""

        return super().update(is_deleted=False, deleted_at=None)

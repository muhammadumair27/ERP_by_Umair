"""Abstract model that provides reversible (soft) deletion."""

from django.db import models
from django.utils import timezone

from common.managers.all_objects_manager import AllObjectsManager
from common.managers.soft_delete_manager import SoftDeleteManager


class SoftDeleteModel(models.Model):
    """Flag rows as deleted instead of removing them from the database."""

    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name="is deleted")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="deleted at")

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft-delete this instance."""

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently remove this instance from the database."""

        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """Undo a previous soft deletion."""

        self.is_deleted = False
        self.deleted_at = None
        self.save()

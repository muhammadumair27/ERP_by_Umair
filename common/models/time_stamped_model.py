"""Abstract model that records creation and last-modification timestamps."""

from django.db import models


class TimeStampedModel(models.Model):
    """Add ``created_at`` and ``updated_at`` audit columns to a model."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        abstract = True

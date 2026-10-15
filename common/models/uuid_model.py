"""Abstract model that uses a UUID primary key."""

import uuid

from django.db import models


class UUIDModel(models.Model):
    """Replace the default integer primary key with a UUID v4."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="id",
    )

    class Meta:
        abstract = True

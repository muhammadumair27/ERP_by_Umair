"""Base class shared by every write-side service."""

from django.db import transaction


class BaseService:
    """Base class for services that mutate state.

    Subclasses wrap their work in ``atomic()`` so a partial failure never
    leaves the database half-written.
    """

    atomic = staticmethod(transaction.atomic)

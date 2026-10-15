"""Base class shared by every read-side selector."""

from django.db.models import QuerySet


class BaseSelector:
    """Base class for objects that build read-only querysets."""

    model = None

    @classmethod
    def get_queryset(cls) -> QuerySet:
        """Return the full queryset for the selector's model."""

        if cls.model is None:
            raise NotImplementedError("Selectors must define a model.")

        return cls.model._default_manager.all()

    @classmethod
    def get_by_id(cls, object_id):
        """Return a single row by primary key, or ``None``."""

        return cls.get_queryset().filter(pk=object_id).first()

"""Provide the canonical UTC timestamp used inside every API envelope."""

from datetime import UTC

from django.utils import timezone as django_timezone


def current_iso_timestamp() -> str:
    """Return the current UTC instant as an ISO-8601 string terminated with ``Z``.

    Example: ``2026-01-15T10:30:00.123456Z``
    """

    return django_timezone.now().astimezone(UTC).isoformat().replace("+00:00", "Z")

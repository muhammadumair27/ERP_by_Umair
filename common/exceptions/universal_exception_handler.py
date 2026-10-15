"""Exception handler that renders every error through the universal envelope."""

from typing import Any

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from common.exceptions.domain_error import DomainError
from common.timestamps.current_iso_timestamp import current_iso_timestamp


def _envelope(message: str, errors: Any, status_code: int) -> dict[str, Any]:
    """Build the universal error envelope."""

    return {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors,
        "status_code": status_code,
        "timestamp": current_iso_timestamp(),
    }


def _flatten(value: Any) -> Any:
    """Convert DRF ``ErrorDetail`` trees into plain JSON-serialisable values."""

    if isinstance(value, ErrorDetail):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _flatten(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_flatten(item) for item in value]
    return value


def _message_from(data: Any, fallback: str) -> str:
    """Derive a readable message from a flattened error payload."""

    if isinstance(data, dict) and data:
        detail = data.get("detail")
        if detail is not None:
            return str(detail)
        first_key, first_value = next(iter(data.items()))
        if isinstance(first_value, (list, tuple)) and first_value:
            return f"{first_key}: {first_value[0]}"
        return f"{first_key}: {first_value}"
    if isinstance(data, (list, tuple)) and data:
        return str(data[0])
    return fallback


def universal_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """Return the universal error envelope for any exception raised by a view."""

    if isinstance(exc, DomainError):
        return Response(_envelope(exc.message, None, exc.status_code), status=exc.status_code)

    if isinstance(exc, DjangoValidationError):
        errors = _flatten(getattr(exc, "message_dict", None) or exc.messages)
        return Response(_envelope("Validation failed", errors, 400), status=400)

    if isinstance(exc, Http404):
        return Response(_envelope("Resource not found", None, 404), status=404)

    if isinstance(exc, DjangoPermissionDenied):
        return Response(_envelope("Permission denied", None, 403), status=403)

    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    data = _flatten(response.data)
    fallback = str(exc.default_detail) if isinstance(exc, APIException) else "An error occurred"

    return Response(
        _envelope(_message_from(data, fallback), data, response.status_code),
        status=response.status_code,
    )

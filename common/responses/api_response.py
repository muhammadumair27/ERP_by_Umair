"""Universal API response envelope.

Every endpoint returns its payload through :class:`APIResponse` so that API
clients always receive the same top-level contract, regardless of the view or
service that produced the data.
"""

from typing import Any

from rest_framework.response import Response

from common.timestamps.current_iso_timestamp import current_iso_timestamp


class APIResponse:
    """Factory for the universal success and error response envelopes."""

    @staticmethod
    def success(
        message: str = "Success",
        data: Any = None,
        status_code: int = 200,
    ) -> Response:
        """Return a success envelope."""

        return Response(
            {
                "success": True,
                "message": message,
                "data": data,
                "errors": None,
                "status_code": status_code,
                "timestamp": current_iso_timestamp(),
            },
            status=status_code,
        )

    @staticmethod
    def created(message: str = "Resource created successfully", data: Any = None) -> Response:
        """Return a ``201 Created`` success envelope."""

        return APIResponse.success(message=message, data=data, status_code=201)

    @staticmethod
    def error(
        message: str = "An error occurred",
        errors: Any = None,
        status_code: int = 400,
    ) -> Response:
        """Return an error envelope."""

        return Response(
            {
                "success": False,
                "message": message,
                "data": None,
                "errors": errors,
                "status_code": status_code,
                "timestamp": current_iso_timestamp(),
            },
            status=status_code,
        )

    @staticmethod
    def validation_error(errors: Any, message: str = "Validation failed") -> Response:
        """Return a ``400`` validation error envelope."""

        return APIResponse.error(message=message, errors=errors, status_code=400)

    @staticmethod
    def not_found(message: str = "Resource not found") -> Response:
        """Return a ``404`` error envelope."""

        return APIResponse.error(message=message, errors=None, status_code=404)

    @staticmethod
    def unauthorized(message: str = "Authentication required") -> Response:
        """Return a ``401`` error envelope."""

        return APIResponse.error(message=message, errors=None, status_code=401)

    @staticmethod
    def forbidden(message: str = "Permission denied") -> Response:
        """Return a ``403`` error envelope."""

        return APIResponse.error(message=message, errors=None, status_code=403)

    @staticmethod
    def conflict(message: str = "Resource already exists") -> Response:
        """Return a ``409`` error envelope."""

        return APIResponse.error(message=message, errors=None, status_code=409)

    @staticmethod
    def server_error(message: str = "Internal server error") -> Response:
        """Return a ``500`` error envelope."""

        return APIResponse.error(message=message, errors=None, status_code=500)

    @staticmethod
    def paginated(
        data: Any,
        pagination: dict[str, Any],
        message: str = "Records retrieved successfully",
    ) -> Response:
        """Return a success envelope carrying a pagination block."""

        return Response(
            {
                "success": True,
                "message": message,
                "data": data,
                "pagination": pagination,
                "errors": None,
                "status_code": 200,
                "timestamp": current_iso_timestamp(),
            },
            status=200,
        )

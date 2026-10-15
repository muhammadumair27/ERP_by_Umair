"""Renderer that guarantees the universal API envelope for every JSON response."""

from typing import Any

from rest_framework.renderers import JSONRenderer

from common.timestamps.current_iso_timestamp import current_iso_timestamp

SCHEMA_PATH_PREFIXES = ("/api/schema", "/api/docs", "/api/redoc")


class UniversalAPIJSONRenderer(JSONRenderer):
    """Wrap every payload in the universal envelope.

    Payloads that already carry the envelope (produced by ``APIResponse`` or by
    ``universal_exception_handler``) pass through untouched. OpenAPI schema and
    documentation endpoints are never wrapped.
    """

    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: dict[str, Any] | None = None,
    ) -> bytes:
        """Render ``data`` as JSON inside the universal envelope."""

        renderer_context = renderer_context or {}
        request = renderer_context.get("request")
        response = renderer_context.get("response")

        path = getattr(request, "path", "") or ""
        if path.startswith(SCHEMA_PATH_PREFIXES):
            return super().render(data, accepted_media_type, renderer_context)

        if isinstance(data, dict) and "success" in data:
            return super().render(data, accepted_media_type, renderer_context)

        status_code = getattr(response, "status_code", 200)

        if status_code in (204, 304):
            return super().render(data, accepted_media_type, renderer_context)

        if status_code < 400:
            payload = {
                "success": True,
                "message": "Operation completed successfully",
                "data": data,
                "errors": None,
                "status_code": status_code,
                "timestamp": current_iso_timestamp(),
            }
        else:
            payload = {
                "success": False,
                "message": self._extract_error_message(data),
                "data": None,
                "errors": data,
                "status_code": status_code,
                "timestamp": current_iso_timestamp(),
            }

        return super().render(payload, accepted_media_type, renderer_context)

    @staticmethod
    def _extract_error_message(data: Any) -> str:
        """Best-effort human readable message for an un-enveloped error payload."""

        if isinstance(data, dict):
            detail = data.get("detail")
            if detail is not None:
                return str(detail)
        if isinstance(data, (list, tuple)) and data:
            return str(data[0])
        return "An error occurred"

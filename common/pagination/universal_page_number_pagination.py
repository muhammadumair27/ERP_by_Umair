"""Pagination that emits the universal paginated envelope."""

from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from common.timestamps.current_iso_timestamp import current_iso_timestamp


class UniversalPageNumberPagination(PageNumberPagination):
    """Page-number pagination whose payload matches the universal contract.

    The default page size comes from ``REST_FRAMEWORK['PAGE_SIZE']`` and callers
    may override it per request with ``?page_size=``.
    """

    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 200

    def get_paginated_response(self, data: Any) -> Response:
        """Return the universal envelope including the pagination block."""

        return Response(
            {
                "success": True,
                "message": "Records retrieved successfully",
                "data": data,
                "pagination": {
                    "count": self.page.paginator.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "page_size": self.get_page_size(self.request),
                    "current_page": self.page.number,
                    "total_pages": self.page.paginator.num_pages,
                },
                "errors": None,
                "status_code": 200,
                "timestamp": current_iso_timestamp(),
            }
        )

    def get_paginated_response_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        """Describe the pagination block for drf-spectacular."""

        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {"type": "string", "example": "Records retrieved successfully"},
                "data": schema,
                "pagination": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer", "example": 100},
                        "next": {"type": "string", "nullable": True},
                        "previous": {"type": "string", "nullable": True},
                        "page_size": {"type": "integer", "example": 20},
                        "current_page": {"type": "integer", "example": 1},
                        "total_pages": {"type": "integer", "example": 5},
                    },
                },
                "errors": {"nullable": True},
                "status_code": {"type": "integer", "example": 200},
                "timestamp": {"type": "string", "format": "date-time"},
            },
        }

"""Domain level exceptions and the universal exception handler."""

from .domain_error import DomainError
from .universal_exception_handler import universal_exception_handler

__all__ = ("DomainError", "universal_exception_handler")

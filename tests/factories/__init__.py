"""factory-boy factories shared across the test suite."""

from .user import DEFAULT_TEST_PASSWORD, UserFactory

__all__ = ("DEFAULT_TEST_PASSWORD", "UserFactory")

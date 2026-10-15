"""Shared pytest fixtures for the Manufacturing ERP test suite."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """Return an unauthenticated DRF API client."""

    return APIClient()


@pytest.fixture
def user(db):
    """Return a persisted active user."""

    return get_user_model().objects.create_user(
        email="fixture-user@example.com",
        password="Str0ng-Test-Passw0rd!",
        full_name="Fixture User",
    )


@pytest.fixture
def authenticated_api_client(api_client: APIClient, user) -> APIClient:
    """Return a DRF API client authenticated as ``user``."""

    api_client.force_authenticate(user=user)
    return api_client

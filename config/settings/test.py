"""Test settings: deterministic, hermetic, and independent of Redis/Celery."""

from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = ["*"]

# Fast password hashing. Never use this outside tests.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "erp-test-cache",
    }
}

DATABASES["default"]["TEST"] = {"NAME": "test_manufacturing_erp"}  # noqa: F405

REST_FRAMEWORK = {  # noqa: F405
    **REST_FRAMEWORK,  # noqa: F405
    "DEFAULT_RENDERER_CLASSES": [
        "common.renderers.universal_api_json_renderer.UniversalAPIJSONRenderer",
    ],
}

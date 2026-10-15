"""Local development settings."""

from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")  # noqa: F405

INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

INTERNAL_IPS = ["127.0.0.1", "::1"]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "config.settings.local.show_debug_toolbar",
    "DISABLE_PANELS": {
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    },
}


def show_debug_toolbar(request) -> bool:  # pragma: no cover - developer helper
    """Show the debug toolbar for local requests only."""

    return bool(DEBUG)

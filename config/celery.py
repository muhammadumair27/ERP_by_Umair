"""Celery application bootstrap for the Manufacturing ERP."""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("manufacturing_erp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:  # pragma: no cover - diagnostic helper
    """Simple task used to verify that a worker is consuming from the broker."""

    print(f"Request: {self.request!r}")  # noqa: T201

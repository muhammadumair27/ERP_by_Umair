#!/usr/bin/env sh
# =============================================================================
# Manufacturing ERP - container entrypoint
# Waits for PostgreSQL, optionally migrates, then execs the container command.
# =============================================================================
set -e

DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.local}"
export DJANGO_SETTINGS_MODULE

wait_for_postgres() {
  echo "Waiting for PostgreSQL to accept connections..."
  python - <<'PY'
import os
import sys
import time

import django
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.local"),
)
django.setup()

for attempt in range(1, 61):
    try:
        connections["default"].ensure_connection()
        print("PostgreSQL is ready.")
        sys.exit(0)
    except OperationalError as exc:
        print(f"  attempt {attempt}/60 failed: {exc}")
        time.sleep(2)

print("PostgreSQL did not become ready in time.", file=sys.stderr)
sys.exit(1)
PY
}

case "${1}" in
  python\ manage.py\ runserver*|python\ manage.py\ migrate*|python\ manage.py\ collectstatic*)
    wait_for_postgres
    ;;
esac

if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
  echo "Applying database migrations..."
  python manage.py migrate --noinput
fi

if [ "${COLLECT_STATIC:-false}" = "true" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

exec "$@"

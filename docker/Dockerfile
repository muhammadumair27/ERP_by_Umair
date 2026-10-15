# syntax=docker/dockerfile:1

# =============================================================================
# Manufacturing ERP - application image
# =============================================================================

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

# --- dependencies -------------------------------------------------------------
FROM base AS dependencies

ARG REQUIREMENTS_FILE=requirements/dev.txt

COPY requirements ./requirements
RUN python -m pip install --upgrade pip \
    && python -m pip install -r "${REQUIREMENTS_FILE}"

# --- runtime ------------------------------------------------------------------
FROM dependencies AS runtime

COPY . .

RUN chmod +x /app/docker/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Manufacturing ERP

Production-grade **Manufacturing ERP backend** built with Django, Django REST Framework,
PostgreSQL, Redis and Celery. The first domain modelled is a cement manufacturer, while the
architecture stays generic enough for textile, FMCG, steel, chemical, food and automotive
manufacturing.

> Current status: **Phase 1 - Foundation (step 1A: bootstrap)**. See
> [`docs/module-status.md`](docs/module-status.md).

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 5.2 LTS |
| API | Django REST Framework 3.18 |
| Database | PostgreSQL 16 |
| Cache / broker | Redis 7 |
| Background jobs | Celery 5.6 + django-celery-beat |
| Auth | JWT (`djangorestframework-simplejwt`), Argon2 password hashing |
| API docs | drf-spectacular (OpenAPI 3, Swagger UI, ReDoc) |
| Containers | Docker + Docker Compose |

---

## Prerequisites

- Python 3.12+
- Docker Desktop (WSL 2 backend on Windows)
- Git

---

## Quickstart (Docker - recommended)

```bash
git clone <repository-url>
cd ERP_by_Umair
cp .env.example .env          # then edit secrets
docker compose up --build
```

Once the stack is healthy:

| URL | Purpose |
|---|---|
| http://localhost:8000/api/v1/ | API root |
| http://localhost:8000/api/docs/ | Swagger UI |
| http://localhost:8000/api/redoc/ | ReDoc |
| http://localhost:8000/api/schema/ | Raw OpenAPI schema |
| http://localhost:8000/admin/ | Django Admin |

Create an administrator:

```bash
docker compose exec web python manage.py createsuperuser
```

Useful commands:

```bash
docker compose logs -f web          # tail application logs
docker compose exec web python manage.py migrate
docker compose exec web python manage.py shell
docker compose down                 # stop
docker compose down -v              # stop and delete volumes
```

---

## Quickstart (local virtualenv)

Requires a reachable PostgreSQL and Redis (for example, `docker compose up postgres redis`).

```bash
python -m venv .venv
.venv\Scripts\activate              # Windows
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py runserver
```

Run the Celery worker and beat in separate terminals:

```bash
celery -A config worker --loglevel=info --pool=solo    # --pool=solo is required on Windows
celery -A config beat --loglevel=info
```

---

## Project layout

```text
config/                 settings split by environment, URLs, Celery, ASGI/WSGI
common/                 cross-cutting building blocks shared by every app
  responses/            universal APIResponse envelope
  renderers/            renderer that enforces the envelope
  exceptions/           domain errors + universal exception handler
  pagination/           universal page-number pagination
  models/               reusable abstract models
  timestamps/           canonical ISO-8601 UTC helper
apps/                   business domains (one package per bounded context)
  accounts/             custom user model and authentication
requirements/           base / dev / prod dependency sets
docker/                 Dockerfile, entrypoint, PostgreSQL bootstrap
tests/                  cross-app test suite and factories
docs/                   architecture and conventions
```

Each app follows the mandatory layout from `AGENTS.md`:

```text
apps/<app>/
  models/          one file per model
  serializers/     one file per serializer
  views/           one ViewSet per file
  services/        business logic (write side)
  selectors/       query logic (read side)
  admin/           Django Admin registration
  migrations/
```

---

## Settings modules

| Module | Usage |
|---|---|
| `config.settings.base` | Shared configuration |
| `config.settings.local` | Local development (`manage.py` default) |
| `config.settings.test` | Test runs |
| `config.settings.production` | Hardened deployment settings |

---

## Conventions

All API responses use the universal envelope:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {},
  "errors": null,
  "status_code": 200,
  "timestamp": "2026-01-15T10:30:00.000000Z"
}
```

Non-negotiable rules (see `AGENTS.md` for the full specification):

- ViewSets only - no `APIView`, no function-based views.
- Business logic lives in services; database access lives in selectors.
- `APIResponse` is mandatory for every response.
- Every model ships with a configured Django Admin.
- Critical operations (inventory, finance, production) are transactional.

---

## Static checks

```bash
ruff check .
python manage.py check
python manage.py makemigrations --check --dry-run
```

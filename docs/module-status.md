# Module Status

Progress tracker for the Manufacturing ERP build.

Legend: `[x]` done - `[~]` in progress - `[ ]` not started

---

## Phase 1 - Foundation

| Step | Scope | Status |
|---|---|---|
| 1A | Bootstrap (config, common layer skeleton, custom user, tooling, Docker) | `[x]` |
| 1B | Common layer (base models, mixins, pagination, filters, permissions) | `[ ]` |
| 1C | Organizations (multi-tenant root model + enforcement) | `[ ]` |
| 1D | Accounts (auth flows, registration, profile, JWT) | `[ ]` |
| 1E | RBAC (Permission, Role, RolePermission, UserRoleAssignment) | `[ ]` |
| 1F | Audit (append-only AuditLog) | `[ ]` |
| 1G | Wrap-up (schema review, docs, CI, final hardening) | `[ ]` |

### 1A - Bootstrap (complete)

- [x] Python 3.12 virtualenv + pinned `requirements/{base,dev,prod}.txt`
- [x] Ruff configuration (`pyproject.toml`)
- [x] Split settings: `base`, `local`, `test`, `production`
- [x] Universal response envelope (`APIResponse`, renderer, exception handler)
- [x] Universal pagination
- [x] Abstract `TimeStampedModel`
- [x] Canonical ISO-8601 UTC timestamp helper
- [x] Custom `accounts.User` model + manager + admin + initial migration
- [x] Docker Compose stack (PostgreSQL, Redis, web, worker, beat)
- [x] Test scaffolding (`tests/` + factory-boy factories)
- [x] `python manage.py check` passes for local / test / production
- [x] `ruff check` and `ruff format --check` pass

---

## Verification notes

Runnable without Docker:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
ruff check .
```

Requires PostgreSQL/Redis (i.e. `docker compose up`):

```bash
python manage.py migrate
python manage.py runserver
```

> `makemigrations` prints a benign `connection timeout expired` warning while the
> database is unavailable; migration generation itself is offline and unaffected.

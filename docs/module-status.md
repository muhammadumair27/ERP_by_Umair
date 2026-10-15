# Module Status

Progress tracker for the Manufacturing ERP build.

Legend: `[x]` done - `[~]` in progress - `[ ]` not started

---

## Deliverables index

| Module | Purpose | Entry points |
|---|---|---|
| `config` | Settings, URLs, ASGI/WSGI, Celery app | `config.settings.local`, `config.urls` |
| `common.responses` | Universal API response envelope | `APIResponse` |
| `common.renderers` | Enforces the envelope on every response | `UniversalAPIJSONRenderer` |
| `common.exceptions` | Domain errors and global handler | `DomainError`, `universal_exception_handler` |
| `common.pagination` | Pagination in envelope format | `UniversalPageNumberPagination` |
| `common.models` | Abstract model bases | `BaseModel`, `UUIDModel`, `TimeStampedModel`, `SoftDeleteModel` |
| `common.querysets` | Soft-delete aware querysets | `SoftDeleteQuerySet` |
| `common.managers` | Soft-delete aware managers | `SoftDeleteManager`, `AllObjectsManager` |
| `common.services` | Write-side base | `BaseService` |
| `common.selectors` | Read-side base | `BaseSelector` |
| `common.validators` | Shared field validators | `validate_phone_number`, `validate_tax_number`, `validate_non_negative_quantity` |
| `apps.accounts` | Custom user model | `User`, `UserManager`, `UserAdmin` |

---

## Phase 1 - Foundation

| Step | Scope | Status |
|---|---|---|
| 1A | Bootstrap (config, common layer skeleton, custom user, tooling, Docker) | `[x]` |
| 1B | Common layer (base models, soft delete, services, selectors, validators) | `[x]` |
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

### 1B - Common layer (complete)

- [x] `UUIDModel` - UUID v4 primary key for domain entities
- [x] `SoftDeleteModel` - reversible deletion (`is_deleted`, `deleted_at`)
- [x] `SoftDeleteQuerySet` - bulk `delete`, `hard_delete`, `alive`, `dead`, `restore`
- [x] `SoftDeleteManager` - default manager that hides deleted rows
- [x] `AllObjectsManager` - manager that includes deleted rows
- [x] `BaseModel` - `UUIDModel` + `TimeStampedModel` + `SoftDeleteModel`
- [x] `BaseService` - shared `atomic()` transaction boundary
- [x] `BaseSelector` - shared read-side query entry point
- [x] Shared validators: phone number, tax number, non-negative quantity
- [x] Runtime introspection probe passes (managers, MRO, inherited fields)

> Design decisions locked in: **UUID primary keys** for domain models,
> **soft delete enabled** by default, **`...Z` ISO-8601 UTC timestamps**.

### 1C - Organizations (not started)

Planned scope:

- `Organization` model (`BaseModel`) - the tenancy root
- `OrganizationMembership` linking user to organization
- Current-organization resolution (middleware / request context)
- `OrganizationScopedModel` abstract base with a mandatory `organization` FK
- `OrganizationScopedSelector` / `OrganizationScopedManager`
- `IsOrganizationMember` and `IsOrganizationAdmin` permissions
- Django Admin registration for every model above

---

## Repository workflow

- `main` - protected: no direct pushes, no force pushes, no deletion, PR required
- `umair` - working branch; every change is pushed here

```bash
git add -A
git commit -m "feat(scope): summary"
git push                      # pushes to umair only
```

Then open a pull request from `umair` into `main` and merge it on GitHub.

---

## Verification notes

Runnable without Docker:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
ruff check .
ruff format --check .
```

Requires PostgreSQL/Redis (i.e. `docker compose up`):

```bash
python manage.py migrate
python manage.py runserver
```

> `makemigrations` prints a benign `connection timeout expired` warning while the
> database is unavailable; migration generation itself is offline and unaffected.

# Data Model: Phase II Web Application

**Feature**: `002-web-auth-specs` | **Date**: 2026-01-05 | **Phase**: II (Full-Stack Web Application)

## Overview
Defines persisted entities supporting authentication and task management. Users come from Better Auth; tasks belong exclusively to one user and enforce isolation via `user_id` filters. This data model implements FR-001 through FR-006 from @specs/features/authentication.md and @specs/features/task-crud-web.md.

## Entities

### User (managed by Better Auth)
| Field | Type | Default | Validation | Source | Notes |
|-------|------|---------|------------|--------|-------|
| id | UUID | generated | required | FR-AUTH-003 | Primary key referenced by tasks |
| email | citext | unique | RFC 5322 compliant | FR-AUTH-002 | Indexed for login |
| password_hash | text | n/a | Argon2/bcrypt | FR-AUTH-001 | Never exposed |
| created_at | timestamptz | now() | required | FR-AUTH-001 | |
| locked_until | timestamptz? | null | >= now | FR-AUTH-008 | For lockouts |

### Task
| Field | Type | Default | Validation | Source | Notes |
|-------|------|---------|------------|--------|-------|
| id | UUID | gen_random_uuid() | required | FR-003 | Primary key |
| user_id | UUID | required | FK → users.id ON DELETE CASCADE | FR-006 | Ensures isolation |
| title | varchar(256) | n/a | non-empty, trimmed | FR-TASK-003 | Indexed |
| description | text? | null | ≤2000 chars | FR-TASK-003 | Optional |
| completed | boolean | false | required | FR-TASK-004 | |
| due_date | date? | null | >= today or null | FR-003 | Optional |
| created_at | timestamptz | now() | required | FR-003 | |
| updated_at | timestamptz | now() | auto update | FR-003 | Trigger or app logic |

## Relationships
- User 1‑to‑N Task via `tasks.user_id`.
- Cascading delete removes tasks when user deleted (per FR-003 isolation guarantee).

## Validation Rules
- `title` must be non-empty and ≤256 characters.
- `description` trimmed to ≤2000 characters.
- `due_date` cannot be in the past when set (client validated, backend enforced).
- `user_id` required on creation and must match authenticated principal.
- Updates must refresh `updated_at` automatically.

## State Transitions (Task)
| Current State | Event | Next State | Notes |
|---------------|-------|------------|-------|
| pending | toggle_complete(true) | completed | PATCH /complete endpoint |
| completed | toggle_complete(false) | pending | PATCH /complete endpoint |
| any | delete | n/a | Row removed |

## SQLModel Snippet
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: constr(min_length=1, max_length=256)
    description: constr(max_length=2000) | None = None
    completed: bool = Field(default=False)
    due_date: date | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Invariants
- Every task row’s `user_id` matches the JWT subject executing the CRUD operation.
- No task operation can change `user_id` (immutable after insert).
- Deleting a user cascades to all associated tasks, preventing orphans.
- `BETTER_AUTH_SECRET` never stored in DB; secrets stay in environment.

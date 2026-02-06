# Database Schema

**Feature Branch**: `002-web-auth-specs`
**Created**: 2026-01-05
**Status**: Draft
**Constitution Reference**: `.specify/memory/constitution.md` v1.0.0

## Overview
Phase II introduces persistent storage for tasks and users using SQLModel backed by Neon Serverless PostgreSQL. The schema must guarantee user isolation by filtering every query through the authenticated user_id. The authentication system (Better Auth) manages the `users` table while our application controls the `tasks` table.

## Entities

### users (managed by Better Auth)
| Column        | Type              | Constraints                                 | Notes                                 |
|---------------|-------------------|---------------------------------------------|---------------------------------------|
| id            | UUID (PK)         | NOT NULL                                    | Provided by Better Auth               |
| email         | citext            | UNIQUE, NOT NULL                            | Indexed for login                     |
| password_hash | text              | NOT NULL                                    | Argon2/bcrypt hash                    |
| created_at    | timestamptz       | NOT NULL DEFAULT now()                      |                                       |
| locked_until  | timestamptz null  | NULLable                                    | For account lockouts                  |

### tasks
| Column        | Type              | Constraints                                 | Notes                                              |
|---------------|-------------------|---------------------------------------------|----------------------------------------------------|
| id            | UUID (PK)         | NOT NULL DEFAULT gen_random_uuid()          | Primary key                                         |
| user_id       | UUID (FK)         | REFERENCES users(id) ON DELETE CASCADE      | Ensures user isolation                              |
| title         | varchar(256)      | NOT NULL                                    | Indexed for search                                  |
| description   | text              | NULLable                                    |                                                    |
| completed     | boolean           | NOT NULL DEFAULT false                      |                                                    |
| due_date      | date              | NULLable                                    | Optional extension of Phase I                       |
| created_at    | timestamptz       | NOT NULL DEFAULT now()                      |                                                    |
| updated_at    | timestamptz       | NOT NULL DEFAULT now()                      | Updated via trigger                                 |

### Indexes
- `idx_tasks_user_id_created_at` on (user_id, created_at desc) for dashboard queries
- `idx_tasks_user_id_status` on (user_id, completed) for filters
- `idx_tasks_user_id_due_date` on (user_id, due_date) for upcoming tasks

## SQLModel Definitions (Conceptual)
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=256)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)
    due_date: date | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Constraints & Invariants
- Every task must reference a valid user_id; cascading delete removes orphan tasks when a user is removed.
- Application queries MUST always filter by `user_id = auth_context.user_id` before returning results.
- `title` must pass validation rules defined in @specs/features/task-crud-web.md.
- Updates to tasks MUST update `updated_at` automatically via trigger or application logic.
- No soft deletes; deletion removes rows permanently.

## Migration Strategy
1. Initial migration creates `tasks` table with indexes and triggers.
2. Migration script runs automatically via Alembic when backend starts in a new environment.
3. Existing Phase I data (in-memory) has no persistence; Phase II will seed sample data via fixtures if needed.
4. Rollback strategy: drop `tasks` table if migration fails before production cutover.

## Query Patterns
- **List tasks**: `SELECT ... FROM tasks WHERE user_id = :user_id ORDER BY created_at DESC LIMIT :limit OFFSET :offset`
- **Search**: `... AND (title ILIKE :q OR description ILIKE :q)` with safe parameterization.
- **Toggle completion**: `UPDATE tasks SET completed = :completed, updated_at = now() WHERE id = :id AND user_id = :user_id`

## Security Considerations
- All database credentials supplied via environment variables (`DATABASE_URL`).
- Only application service account has access to `tasks`; no shared credentials.
- Periodic secret rotation for DB password as mandated by infrastructure policy.

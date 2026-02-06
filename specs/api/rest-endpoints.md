# REST API Endpoints

**Feature Branch**: `002-web-auth-specs`
**Created**: 2026-01-05
**Status**: Draft
**Constitution Reference**: `.specify/memory/constitution.md` v1.0.0

## Base URL & Authentication
- Base path: `/api/v1`
- All endpoints require HTTPS in production.
- Authentication: `Authorization: Bearer <JWT>` header provided by Better Auth (see @specs/features/authentication.md).
- Unauthenticated requests MUST receive HTTP 401 with `WWW-Authenticate: Bearer`.

## Common Schemas (Pydantic-style)
```python
class TaskCreate(BaseModel):
    title: constr(min_length=1, max_length=256)
    description: constr(max_length=2000) | None = None
    due_date: date | None = None

class TaskUpdate(BaseModel):
    title: constr(min_length=1, max_length=256) | None = None
    description: constr(max_length=2000) | None = None
    due_date: date | None = None

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    completed: bool
    due_date: date | None
    created_at: datetime
    updated_at: datetime

class ErrorResponse(BaseModel):
    detail: str
    code: Literal["NOT_FOUND", "UNAUTHORIZED", "FORBIDDEN", "VALIDATION_ERROR", "SERVER_ERROR"]
```

## Endpoints

### POST /api/v1/tasks
Create a task for the authenticated user.

- **Auth**: Required
- **Body**: `TaskCreate`
- **Responses**:
  - `201 Created`: Returns `TaskResponse`
  - `400 Bad Request`: Invalid payload
  - `401 Unauthorized`: Missing/invalid token

### GET /api/v1/tasks
List tasks belonging to the authenticated user with optional filters.

- **Auth**: Required
- **Query Params**:
  - `status`: `pending | completed`
  - `search`: substring match on title/description
  - `sort_by`: `created_at | due_date | title` (default `created_at`)
  - `sort_dir`: `asc | desc` (default `desc`)
  - `limit`: 1–100 (default 50)
  - `offset`: 0+
- **Responses**:
  - `200 OK`: `{ "items": [TaskResponse], "total": int, "limit": int, "offset": int }`
  - `401 Unauthorized`

### GET /api/v1/tasks/{id}
Fetch a specific task owned by the authenticated user.

- **Auth**: Required
- **Path Params**: `id: UUID`
- **Responses**:
  - `200 OK`: `TaskResponse`
  - `404 Not Found`: Task does not exist or belongs to another user
  - `401 Unauthorized`

### PUT /api/v1/tasks/{id}
Replace a task’s editable fields.

- **Auth**: Required
- **Body**: `TaskUpdate` (at least one field required)
- **Responses**:
  - `200 OK`: Updated `TaskResponse`
  - `400 Bad Request`: Invalid payload
  - `404 Not Found`: Task not owned by requester
  - `401 Unauthorized`

### DELETE /api/v1/tasks/{id}
Delete a task owned by the authenticated user.

- **Auth**: Required
- **Responses**:
  - `204 No Content`
  - `404 Not Found`
  - `401 Unauthorized`

### PATCH /api/v1/tasks/{id}/complete
Toggle completion state for a task.

- **Auth**: Required
- **Body**: `{ "completed": bool }`
- **Responses**:
  - `200 OK`: Updated `TaskResponse`
  - `404 Not Found`
  - `401 Unauthorized`

## Error Responses
| HTTP Status | Code              | Description                                               |
|-------------|-------------------|-----------------------------------------------------------|
| 400         | VALIDATION_ERROR  | Payload fails schema or business validation               |
| 401         | UNAUTHORIZED      | Missing/invalid/expired token                             |
| 403         | FORBIDDEN         | Token valid but lacks permission (future roles)           |
| 404         | NOT_FOUND         | Resource does not exist or not owned by requester         |
| 409         | CONFLICT          | Uniqueness constraint violation (e.g., duplicate title)   |
| 429         | RATE_LIMITED      | Client exceeded allowed request rate                      |
| 500         | SERVER_ERROR      | Unexpected server failure                                 |

All error responses must include `trace_id` metadata for observability.

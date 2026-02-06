# Contract: Task REST API

## Endpoint Summary
| Method | Path | Description | Auth | Status Codes |
|--------|------|-------------|------|--------------|
| POST | /api/v1/tasks | Create task | Bearer JWT | 201, 400, 401 |
| GET | /api/v1/tasks | List tasks | Bearer JWT | 200, 401 |
| GET | /api/v1/tasks/{id} | Fetch task | Bearer JWT | 200, 401, 404 |
| PUT | /api/v1/tasks/{id} | Replace task | Bearer JWT | 200, 400, 401, 404 |
| PATCH | /api/v1/tasks/{id}/complete | Toggle completion | Bearer JWT | 200, 401, 404 |
| DELETE | /api/v1/tasks/{id} | Delete task | Bearer JWT | 204, 401, 404 |

## POST /api/v1/tasks
Request:
```json
{
  "title": "Pay bills",
  "description": "Internet + electricity",
  "due_date": "2026-01-10"
}
```
Response 201:
```json
{
  "id": "uuid",
  "title": "Pay bills",
  "description": "Internet + electricity",
  "completed": false,
  "due_date": "2026-01-10",
  "created_at": "2026-01-05T12:34:00Z",
  "updated_at": "2026-01-05T12:34:00Z"
}
```

## GET /api/v1/tasks
Query params: `status`, `search`, `sort_by`, `sort_dir`, `limit`, `offset`
Response 200:
```json
{
  "items": [TaskResponse...],
  "total": 25,
  "limit": 20,
  "offset": 0
}
```

## Error Payload
```json
{
  "detail": "Task not found",
  "code": "NOT_FOUND",
  "trace_id": "abc123"
}
```

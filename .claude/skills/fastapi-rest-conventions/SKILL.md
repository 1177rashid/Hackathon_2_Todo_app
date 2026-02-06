---
name: fastapi-rest-conventions
description: Standardized FastAPI backend patterns for Phase 2 full-stack app. Automatically activates when discussing FastAPI routes, API endpoints, SQLModel integration, dependency injection, or REST API design.
---

# FastAPI REST Conventions Expert

You are the official FastAPI Backend Expert for this Hackathon II Todo project (Phase 2). Your responsibility is to ensure clean, consistent, production-ready FastAPI code following modern best practices.

## When to Activate

This skill automatically activates when the user mentions:
- Building Phase 2 backend API
- FastAPI routes, endpoints, or routers
- SQLModel database integration
- Pydantic models and validation
- Dependency injection patterns
- HTTPException and error handling
- Async/await patterns in FastAPI
- CORS configuration
- API documentation (Swagger/OpenAPI)

## Core Principles

1. **RESTful Design**: Follow REST conventions for route naming and HTTP methods
2. **Type Safety**: Leverage Pydantic models for automatic validation
3. **Async First**: Use async/await for all database operations
4. **User Isolation**: Every query MUST filter by user_id from JWT
5. **Error Handling**: Consistent HTTPException usage with proper status codes
6. **Dependency Injection**: Use FastAPI dependencies for auth, DB sessions
7. **Documentation**: Auto-generated OpenAPI docs with clear descriptions
8. **Testing**: Each endpoint has integration tests

## Phase 2 Backend Project Structure

```
hackathon-todo-app/
├── backend/                      # FastAPI application
│   ├── __init__.py
│   ├── main.py                  # FastAPI app initialization
│   ├── config.py                # Settings (Pydantic BaseSettings)
│   ├── database.py              # Database connection and session
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py              # SQLModel Task model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py              # Pydantic request/response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py             # Task CRUD endpoints
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py              # JWT verification dependency
│   │   └── database.py          # DB session dependency
│   └── exceptions.py            # Custom exception handlers
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_tasks.py            # Task endpoint tests
│   └── test_auth.py             # Auth middleware tests
├── alembic/                      # Database migrations
│   ├── versions/
│   └── env.py
├── requirements.txt
├── .env.example
└── README.md
```

## Database Configuration

```python
# backend/database.py
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from .config import settings

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10
)

def create_db_and_tables():
    """Create all database tables. Call on startup."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Automatically handles commit/rollback and cleanup.
    """
    with Session(engine) as session:
        yield session
```

## Configuration Pattern

```python
# backend/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database
    DATABASE_URL: str

    # JWT Authentication (shared with Better Auth)
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    # Application
    APP_NAME: str = "Hackathon Todo API"
    DEBUG: bool = False

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()

settings = get_settings()
```

## SQLModel Task Model

```python
# backend/models/task.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Task(SQLModel, table=True):
    """
    Task database model with user isolation.
    All queries MUST filter by user_id.
    """
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)  # From JWT claims
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user_abc123",
                "title": "Complete hackathon project",
                "description": "Build full-stack Todo app with Next.js and FastAPI",
                "is_completed": False,
                "created_at": "2025-01-02T10:30:00Z",
                "updated_at": "2025-01-02T10:30:00Z"
            }
        }
```

## Pydantic Request/Response Schemas

```python
# backend/schemas/task.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional

class TaskCreate(BaseModel):
    """Request schema for creating a task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Complete hackathon project",
                "description": "Build full-stack Todo app"
            }
        }
    )

class TaskUpdate(BaseModel):
    """Request schema for updating a task (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    is_completed: Optional[bool] = None

class TaskResponse(BaseModel):
    """Response schema for a single task."""
    id: UUID
    user_id: str
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskListResponse(BaseModel):
    """Response schema for list of tasks."""
    tasks: list[TaskResponse]
    total: int

class ErrorResponse(BaseModel):
    """Standard error response schema."""
    detail: str
    error_code: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Task not found",
                "error_code": "TASK_NOT_FOUND"
            }
        }
    )
```

## JWT Authentication Dependency

```python
# backend/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredential
import jwt
from ..config import settings

security = HTTPBearer()

def get_current_user_id(
    credentials: HTTPAuthCredential = Depends(security)
) -> str:
    """
    Extract and verify JWT token, return user_id.

    This dependency should be used on ALL protected routes.

    Args:
        credentials: JWT token from Authorization header

    Returns:
        user_id extracted from JWT claims

    Raises:
        HTTPException 401: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        # Verify JWT with shared secret from Better Auth
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Extract user_id from claims
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

## Task Router with CRUD Operations

```python
# backend/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from uuid import UUID
from typing import Optional

from ..database import get_session
from ..dependencies.auth import get_current_user_id
from ..models.task import Task
from ..schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse
)

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={
        401: {"description": "Unauthorized - Invalid or missing JWT token"},
        500: {"description": "Internal server error"}
    }
)

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user"
)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> Task:
    """
    Create a new task.

    - **title**: Task title (required, 1-200 chars)
    - **description**: Optional description (max 1000 chars)

    Returns the created task with generated ID and timestamps.
    """
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.get(
    "",
    response_model=TaskListResponse,
    summary="List all tasks",
    description="Get all tasks for the authenticated user, optionally filtered by completion status"
)
async def list_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskListResponse:
    """
    List all tasks for the current user.

    Query parameters:
    - **completed**: Optional filter (true/false for completed/incomplete tasks)

    Returns tasks sorted by created_at descending (newest first).
    """
    # Base query with user isolation
    query = select(Task).where(Task.user_id == user_id)

    # Apply completion filter if provided
    if completed is not None:
        query = query.where(Task.is_completed == completed)

    # Order by newest first
    query = query.order_by(Task.created_at.desc())

    tasks = session.exec(query).all()

    return TaskListResponse(tasks=tasks, total=len(tasks))

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    responses={
        404: {"description": "Task not found"}
    }
)
async def get_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> Task:
    """
    Get a specific task by ID.

    Returns 404 if task doesn't exist or doesn't belong to the user.
    """
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    return task

@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    responses={
        404: {"description": "Task not found"}
    }
)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> Task:
    """
    Update an existing task.

    All fields are optional. Only provided fields will be updated.
    """
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update timestamp
    from datetime import datetime
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    responses={
        404: {"description": "Task not found"}
    }
)
async def delete_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a task permanently.

    Returns 204 No Content on success.
    """
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    session.delete(task)
    session.commit()

@router.post(
    "/{task_id}/complete",
    response_model=TaskResponse,
    summary="Mark task as completed",
    responses={
        404: {"description": "Task not found"}
    }
)
async def complete_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> Task:
    """
    Mark a task as completed.

    Convenience endpoint for common action.
    """
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    task.is_completed = True
    from datetime import datetime
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.get(
    "/stats/summary",
    summary="Get task statistics",
    description="Get summary statistics for the user's tasks"
)
async def get_task_stats(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> dict:
    """
    Get task statistics for the current user.

    Returns total, completed, and incomplete counts.
    """
    query = select(Task).where(Task.user_id == user_id)
    all_tasks = session.exec(query).all()

    total = len(all_tasks)
    completed = len([t for t in all_tasks if t.is_completed])

    return {
        "total": total,
        "completed": completed,
        "incomplete": total - completed
    }
```

## FastAPI Application Setup

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .database import create_db_and_tables
from .routers import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: create database tables
    create_db_and_tables()
    yield
    # Shutdown: cleanup if needed

app = FastAPI(
    title=settings.APP_NAME,
    description="Hackathon II Todo API - Phase 2 Backend",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "2.0.0"}
```

## Error Handling Best Practices

```python
# backend/exceptions.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors (e.g., unique constraint violations)."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Database integrity error. Resource may already exist.",
            "error_code": "INTEGRITY_ERROR"
        }
    )

# Register in main.py:
# app.add_exception_handler(IntegrityError, integrity_error_handler)
```

## Testing Pattern

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from backend.main import app
from backend.database import get_session
from backend.dependencies.auth import get_current_user_id

# Test database setup
@pytest.fixture(name="session")
def session_fixture():
    """Create a fresh in-memory database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with mocked auth and database."""
    def get_session_override():
        return session

    def get_user_id_override():
        return "test_user_123"

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user_id] = get_user_id_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()

# tests/test_tasks.py
def test_create_task(client: TestClient):
    """Test creating a new task."""
    response = client.post(
        "/api/tasks",
        json={"title": "Test task", "description": "Test description"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["user_id"] == "test_user_123"
    assert "id" in data

def test_list_tasks(client: TestClient):
    """Test listing tasks."""
    # Create tasks
    client.post("/api/tasks", json={"title": "Task 1"})
    client.post("/api/tasks", json={"title": "Task 2"})

    # List all tasks
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["tasks"]) == 2

def test_update_task(client: TestClient):
    """Test updating a task."""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Original"}
    )
    task_id = create_response.json()["id"]

    # Update task
    update_response = client.patch(
        f"/api/tasks/{task_id}",
        json={"title": "Updated"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated"

def test_delete_task(client: TestClient):
    """Test deleting a task."""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "To delete"}
    )
    task_id = create_response.json()["id"]

    # Delete task
    delete_response = client.delete(f"/api/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Verify deleted
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404
```

## RESTful Route Naming Conventions

Follow these patterns for consistent API design:

| HTTP Method | Route                | Purpose                    | Status Code |
|-------------|----------------------|----------------------------|-------------|
| POST        | /api/tasks           | Create new task            | 201         |
| GET         | /api/tasks           | List all tasks             | 200         |
| GET         | /api/tasks/{id}      | Get single task            | 200         |
| PATCH       | /api/tasks/{id}      | Update task (partial)      | 200         |
| PUT         | /api/tasks/{id}      | Replace task (full)        | 200         |
| DELETE      | /api/tasks/{id}      | Delete task                | 204         |
| POST        | /api/tasks/{id}/complete | Mark complete (action) | 200         |

## Common Mistakes to Avoid

❌ **No user isolation**: `select(Task).all()` (returns ALL users' tasks!)
✅ **Always filter by user_id**: `select(Task).where(Task.user_id == user_id)`

❌ **Generic error messages**: `raise HTTPException(400, "Error")`
✅ **Specific error details**: `raise HTTPException(404, f"Task {task_id} not found")`

❌ **Missing status codes**: Just return data
✅ **Explicit status codes**: `status_code=status.HTTP_201_CREATED`

❌ **No response models**: Return raw dictionaries
✅ **Pydantic schemas**: `response_model=TaskResponse`

❌ **Sync database calls**: `session.query()` blocking
✅ **Async patterns**: Use `async def` for all endpoints

## Judge Evaluation Checklist

For a high-scoring Phase 2 backend:
- [ ] All routes protected with JWT authentication
- [ ] User isolation enforced on ALL database queries
- [ ] Proper HTTP status codes (201, 204, 400, 401, 404, 500)
- [ ] Pydantic models for request/response validation
- [ ] Auto-generated OpenAPI documentation at /docs
- [ ] Comprehensive error handling with HTTPException
- [ ] Integration tests with >80% coverage
- [ ] CORS configured for Next.js frontend
- [ ] Environment variables for secrets (no hardcoded values)
- [ ] Database migrations with Alembic

## Integration with Other Skills

- **spec-writing**: API specs define the routes you implement
- **jwt-auth-best-practices**: Provides the get_current_user_id dependency
- **python-cli-patterns**: Phase 1 TaskManager logic → Phase 2 route handlers
- **nextjs-app-router-patterns**: Backend routes consumed by frontend API client

Build a backend that judges will love: type-safe, well-documented, and secure!

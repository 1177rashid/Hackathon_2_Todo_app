---
name: jwt-auth-best-practices
description: Secure JWT integration with Better Auth for Phase 2 multi-user support. Automatically activates when discussing authentication, JWT tokens, Better Auth, token verification, user isolation, or security middleware.
---

# JWT Authentication Best Practices Expert

You are the official Authentication and Security Expert for this Hackathon II Todo project (Phase 2). Your responsibility is to ensure secure JWT-based authentication with proper user isolation and zero security vulnerabilities.

## When to Activate

This skill automatically activates when the user mentions:
- JWT authentication or token verification
- Better Auth integration
- User isolation or multi-user support
- Authorization middleware
- Extracting user_id from tokens
- Token expiration or refresh
- Security vulnerabilities (XSS, CSRF, injection)
- Protected routes or endpoints
- 401 Unauthorized errors

## Core Security Principles

1. **Never Trust the Client**: Always verify JWT on the backend
2. **User Isolation is Mandatory**: Every database query MUST filter by user_id
3. **Fail Securely**: Return 401 for any authentication failure
4. **Shared Secret Protection**: Never expose JWT secret in code or version control
5. **Token Validation**: Verify signature, expiration, and required claims
6. **HTTPS Only**: Production must use HTTPS for token transmission
7. **No Token in URL**: JWT only in Authorization header, never query params
8. **Principle of Least Privilege**: Users can only access their own data

## Better Auth + FastAPI Integration Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Next.js       │      │   Better Auth    │      │   FastAPI       │
│   Frontend      │─────▶│   Auth Server    │      │   Backend       │
│                 │      │   (JWT issuer)   │      │   (JWT verifier)│
└─────────────────┘      └──────────────────┘      └─────────────────┘
       │                          │                          │
       │  1. Login request        │                          │
       │─────────────────────────▶│                          │
       │                          │                          │
       │  2. JWT token (signed)   │                          │
       │◀─────────────────────────│                          │
       │                          │                          │
       │  3. API request + JWT    │                          │
       │────────────────────────────────────────────────────▶│
       │                          │                          │
       │                          │  4. Verify JWT signature │
       │                          │     (shared secret)      │
       │                          │◀─────────────────────────│
       │                          │                          │
       │  5. Response (user data) │                          │
       │◀────────────────────────────────────────────────────│
       │                          │                          │
```

**Key Points:**
- Better Auth issues JWTs signed with shared secret
- FastAPI verifies JWTs using the SAME shared secret
- user_id is extracted from JWT claims (typically `sub` field)
- All protected routes require valid JWT

## Environment Configuration

```bash
# .env (NEVER commit this file!)
# Shared between Better Auth and FastAPI

# Database
DATABASE_URL=postgresql://user:password@neon-host/dbname

# JWT Configuration (MUST match Better Auth settings)
JWT_SECRET=your-super-secret-key-min-32-chars  # Same secret for both systems
JWT_ALGORITHM=HS256                             # Symmetric algorithm (HS256)
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# Better Auth Configuration
BETTER_AUTH_URL=http://localhost:3000/api/auth
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars  # Same as JWT_SECRET

# Application
ALLOWED_ORIGINS=http://localhost:3000
DEBUG=false
```

```bash
# .env.example (Safe to commit - no actual secrets)
DATABASE_URL=postgresql://user:password@host/dbname
JWT_SECRET=change-me-in-production
JWT_ALGORITHM=HS256
BETTER_AUTH_URL=http://localhost:3000/api/auth
ALLOWED_ORIGINS=http://localhost:3000
```

## Pydantic Settings for Configuration

```python
# backend/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings with JWT configuration.
    All sensitive values loaded from environment variables.
    """
    # Database
    DATABASE_URL: str

    # JWT Settings (shared with Better Auth)
    JWT_SECRET: str  # CRITICAL: Must match Better Auth secret
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Better Auth
    BETTER_AUTH_URL: str
    BETTER_AUTH_SECRET: str  # Usually same as JWT_SECRET

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # Application
    APP_NAME: str = "Hackathon Todo API"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

    def validate_jwt_secret(self):
        """Ensure JWT secret is strong enough."""
        if len(self.JWT_SECRET) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters")
        if self.JWT_SECRET == "change-me-in-production":
            raise ValueError("JWT_SECRET must be changed in production")

@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance (computed once)."""
    settings = Settings()
    settings.validate_jwt_secret()
    return settings

settings = get_settings()
```

## JWT Verification Dependency

```python
# backend/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredential
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from typing import Annotated

from ..config import settings

# HTTP Bearer token scheme (extracts from Authorization header)
security = HTTPBearer(
    scheme_name="JWT Bearer Token",
    description="JWT token from Better Auth login"
)

def get_current_user_id(
    credentials: HTTPAuthCredential = Depends(security)
) -> str:
    """
    Extract and verify JWT token from Authorization header.

    This dependency MUST be used on ALL protected routes.

    Security checks performed:
    1. Token signature verification (using shared secret)
    2. Token expiration check
    3. Required claims validation (sub = user_id)

    Args:
        credentials: JWT token from "Authorization: Bearer <token>" header

    Returns:
        user_id (str): Extracted from JWT 'sub' claim

    Raises:
        HTTPException 401: If token is missing, invalid, or expired

    Example usage:
        @router.get("/api/tasks")
        async def list_tasks(user_id: str = Depends(get_current_user_id)):
            # user_id is now verified and safe to use
            tasks = get_user_tasks(user_id)
            return tasks
    """
    token = credentials.credentials

    try:
        # Decode and verify JWT signature
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            # Optional: Add audience/issuer verification
            # audience="your-app",
            # issuer="better-auth"
        )

        # Extract user_id from 'sub' claim (JWT standard)
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID (sub claim)",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Optional: Additional claims validation
        # email = payload.get("email")
        # roles = payload.get("roles", [])

        return user_id

    except ExpiredSignatureError:
        # Token has expired - user needs to re-authenticate
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except InvalidTokenError as e:
        # Token signature invalid or malformed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception as e:
        # Unexpected error - fail securely
        # Log this in production for debugging
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Type alias for cleaner route signatures
CurrentUserID = Annotated[str, Depends(get_current_user_id)]

# Usage example with type alias:
# async def my_route(user_id: CurrentUserID):
#     ...
```

## User Isolation in Database Queries

**CRITICAL RULE:** Every database query that accesses user data MUST filter by user_id.

### ✅ Correct: User Isolation Enforced

```python
# GET /api/tasks - List user's tasks
@router.get("/api/tasks")
async def list_tasks(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # CORRECT: Filter by authenticated user's ID
    query = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(query).all()
    return {"tasks": tasks}

# GET /api/tasks/{task_id} - Get single task
@router.get("/api/tasks/{task_id}")
async def get_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)

    # CORRECT: Verify task belongs to user
    if not task or task.user_id != user_id:
        raise HTTPException(404, "Task not found")

    return task

# POST /api/tasks - Create task
@router.post("/api/tasks")
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # CORRECT: Assign user_id from JWT (never from request body!)
    task = Task(
        user_id=user_id,  # From authenticated token
        title=task_data.title,
        description=task_data.description
    )
    session.add(task)
    session.commit()
    return task
```

### ❌ SECURITY VULNERABILITIES: Never Do This!

```python
# VULNERABILITY 1: No user isolation - returns ALL users' tasks!
@router.get("/api/tasks")
async def list_tasks_INSECURE(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()  # ❌ CRITICAL BUG
    return {"tasks": tasks}

# VULNERABILITY 2: No user verification - any user can access any task!
@router.get("/api/tasks/{task_id}")
async def get_task_INSECURE(
    task_id: UUID,
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)  # ❌ No user_id check
    return task

# VULNERABILITY 3: User ID from request body - client can impersonate others!
@router.post("/api/tasks")
async def create_task_INSECURE(
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    task = Task(
        user_id=task_data.user_id,  # ❌ NEVER trust client input for user_id
        title=task_data.title
    )
    session.add(task)
    session.commit()
    return task

# VULNERABILITY 4: No authentication - anyone can access
@router.get("/api/tasks")
async def list_tasks_NO_AUTH(session: Session = Depends(get_session)):
    # ❌ Missing Depends(get_current_user_id) - route is public!
    tasks = session.exec(select(Task)).all()
    return {"tasks": tasks}
```

## Protected Route Pattern

```python
# backend/routers/tasks.py
from fastapi import APIRouter, Depends
from ..dependencies.auth import get_current_user_id, CurrentUserID

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    # Apply authentication to ALL routes in this router
    dependencies=[Depends(get_current_user_id)]
)

# Option 1: Route-level authentication
@router.get("")
async def list_tasks(
    user_id: str = Depends(get_current_user_id),  # Explicit dependency
    session: Session = Depends(get_session)
):
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return {"tasks": tasks}

# Option 2: Using type alias for cleaner code
@router.post("")
async def create_task(
    task_data: TaskCreate,
    user_id: CurrentUserID,  # Cleaner syntax with type alias
    session: Session = Depends(get_session)
):
    task = Task(user_id=user_id, **task_data.model_dump())
    session.add(task)
    session.commit()
    return task
```

## Error Handling for Auth Failures

```python
# backend/exceptions.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

async def jwt_error_handler(request: Request, exc: Exception):
    """
    Custom handler for JWT errors.
    Returns consistent error format.
    """
    if isinstance(exc, ExpiredSignatureError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": "Token has expired",
                "error_code": "TOKEN_EXPIRED",
                "action": "Please log in again"
            },
            headers={"WWW-Authenticate": "Bearer"}
        )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Invalid authentication credentials",
            "error_code": "INVALID_TOKEN"
        },
        headers={"WWW-Authenticate": "Bearer"}
    )

# Register in main.py:
# app.add_exception_handler(InvalidTokenError, jwt_error_handler)
# app.add_exception_handler(ExpiredSignatureError, jwt_error_handler)
```

## Frontend Integration Pattern

```typescript
// frontend/lib/api-client.ts
class ApiClient {
  private baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  /**
   * Make authenticated request to backend API.
   * Automatically includes JWT token from Better Auth session.
   */
  async authenticatedRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    // Get JWT token from Better Auth session (client-side)
    const token = await this.getSessionToken();

    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,  // Include JWT
        ...options.headers,
      },
    });

    if (response.status === 401) {
      // Token expired or invalid - redirect to login
      window.location.href = '/login';
      throw new Error('Authentication failed');
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Request failed');
    }

    return response.json();
  }

  private async getSessionToken(): Promise<string | null> {
    // Better Auth provides session with JWT token
    // Implementation depends on Better Auth setup
    const session = await getSession();  // Better Auth function
    return session?.accessToken || null;
  }

  // Example: Get user's tasks
  async getTasks() {
    return this.authenticatedRequest<{ tasks: Task[] }>('/api/tasks');
  }

  // Example: Create task
  async createTask(data: { title: string; description?: string }) {
    return this.authenticatedRequest<Task>('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export const apiClient = new ApiClient();
```

## Testing Authentication

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
import jwt
from datetime import datetime, timedelta

def create_test_token(user_id: str, expired: bool = False) -> str:
    """Helper to create test JWT tokens."""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(
            minutes=-5 if expired else 60
        )
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def test_protected_route_without_token(client: TestClient):
    """Test that protected routes reject requests without token."""
    response = client.get("/api/tasks")
    assert response.status_code == 403  # FastAPI HTTPBearer returns 403

def test_protected_route_with_invalid_token(client: TestClient):
    """Test that invalid tokens are rejected."""
    response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]

def test_protected_route_with_expired_token(client: TestClient):
    """Test that expired tokens are rejected."""
    expired_token = create_test_token("user_123", expired=True)
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert "expired" in response.json()["detail"].lower()

def test_protected_route_with_valid_token(client: TestClient):
    """Test that valid tokens grant access."""
    valid_token = create_test_token("user_123")
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200

def test_user_isolation(client: TestClient, session: Session):
    """Test that users can only access their own data."""
    # Create tasks for two different users
    user1_token = create_test_token("user_1")
    user2_token = create_test_token("user_2")

    # User 1 creates task
    response1 = client.post(
        "/api/tasks",
        json={"title": "User 1 task"},
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    task1_id = response1.json()["id"]

    # User 2 tries to access User 1's task
    response2 = client.get(
        f"/api/tasks/{task1_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert response2.status_code == 404  # Not found (user isolation)

    # User 1 can access their own task
    response3 = client.get(
        f"/api/tasks/{task1_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response3.status_code == 200
```

## Security Checklist

Before submitting Phase 2, verify:

### JWT Configuration
- [ ] JWT_SECRET is at least 32 characters
- [ ] JWT_SECRET is loaded from environment variable (not hardcoded)
- [ ] JWT_SECRET matches between Better Auth and FastAPI
- [ ] .env file is in .gitignore (never committed)
- [ ] .env.example exists with placeholder values

### Authentication Middleware
- [ ] HTTPBearer dependency extracts token from Authorization header
- [ ] JWT signature is verified on every request
- [ ] Token expiration is checked
- [ ] user_id (sub claim) is validated as non-null
- [ ] Auth failures return 401 with clear error messages

### User Isolation
- [ ] ALL database queries filter by user_id
- [ ] user_id is extracted from JWT (never from request body)
- [ ] Single-resource routes verify task.user_id == current_user_id
- [ ] Users cannot access other users' data (verified with tests)

### API Routes
- [ ] ALL protected routes use Depends(get_current_user_id)
- [ ] No routes accidentally left public
- [ ] Create operations assign user_id from JWT
- [ ] Update/Delete operations verify ownership

### Error Handling
- [ ] 401 for authentication failures
- [ ] 403 for missing Authorization header (HTTPBearer default)
- [ ] 404 for resources not found OR not owned by user
- [ ] No sensitive information in error messages

### Testing
- [ ] Tests for missing token (403/401)
- [ ] Tests for invalid token (401)
- [ ] Tests for expired token (401)
- [ ] Tests for user isolation (404 for other user's data)
- [ ] Tests for valid authentication (200/201)

## Common Mistakes to Avoid

❌ **Hardcoded secrets**: `JWT_SECRET = "my-secret-key"`
✅ **Environment variables**: `JWT_SECRET = os.getenv("JWT_SECRET")`

❌ **Trusting client user_id**: `user_id = request_body.user_id`
✅ **JWT-verified user_id**: `user_id = Depends(get_current_user_id)`

❌ **No expiration check**: Token valid forever
✅ **Expiration enforced**: `jwt.decode()` automatically checks `exp` claim

❌ **Generic errors**: "Unauthorized"
✅ **Specific errors**: "Token has expired. Please log in again."

❌ **Inconsistent filtering**: Some queries forget user_id filter
✅ **Always filter**: Every query includes `.where(Task.user_id == user_id)`

❌ **Token in URL**: `/api/tasks?token=abc123`
✅ **Token in header**: `Authorization: Bearer abc123`

## Integration with Other Skills

- **spec-writing**: Security requirements documented in specs
- **fastapi-rest-conventions**: Auth dependency used in all protected routes
- **python-cli-patterns**: Phase 1 has no auth; Phase 2 adds user_id
- **nextjs-app-router-patterns**: Frontend sends JWT in Authorization header

Build a backend that judges can't break: secure by design, tested thoroughly!

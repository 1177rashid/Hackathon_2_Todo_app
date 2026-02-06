# Research: Phase II Web Application

## Decision 1: Monorepo with Dedicated frontend/ and backend/
- **Rationale**: Keeps Next.js and FastAPI isolated yet versioned together so spec-driven outputs remain aligned with shared contracts. Enables separate deployment targets (Vercel + containerized API) while sharing tooling (lint, formatting, CI) at the root.
- **Alternatives Considered**:
  - *Single FastAPI project serving SSR UI*: Rejected because constitution mandates Next.js for web UI and this would blur separation of concerns.
  - *Two independent repos*: Rejected because Phase II requires synchronized releases and centralized specs/tasks.

## Decision 2: Better Auth issuing JWTs, FastAPI verifying via middleware
- **Rationale**: Constitution already mandates Better Auth + JWT. Client-side issuance keeps frontend UX responsive while backend verifies statelessly using shared `BETTER_AUTH_SECRET`. Aligns with @specs/features/authentication.md.
- **Alternatives Considered**:
  - *Session cookies stored on backend*: Rejected because services must remain stateless.
  - *3rd-party IdP (OAuth/social)*: Deferred beyond Phase II scope.

## Decision 3: SQLModel + Neon PostgreSQL for persistence
- **Rationale**: Constitution enforces SQLModel + Neon when persistence is introduced. SQLModel integrates cleanly with FastAPI and provides typing plus Alembic support. Neon serverless fits stateless scaling goals.
- **Alternatives Considered**:
  - *Supabase or PlanetScale*: Violates constitutional DB choice.
  - *Plain SQLAlchemy models*: Less ergonomic with FastAPI dependency injection.

## Decision 4: REST API design (versioned /api/v1, user_id derived from JWT)
- **Rationale**: Aligns with @specs/api/rest-endpoints.md and simplifies clients—no user_id leakage over the wire. Versioning future-proofs Phase III additions.
- **Alternatives Considered**:
  - *GraphQL*: Overkill for current CRUD scope and not specified.
  - *Including user_id in URLs*: Risks user enumeration and duplicates authorization checks.

## Decision 5: State management via React Query (or SWR) + optimistic UI
- **Rationale**: Phase II UI requires responsive feedback; data fetching hooks with cache invalidation minimize boilerplate and deliver real-time feel mandated in @specs/features/task-crud-web.md.
- **Alternatives Considered**:
  - *Redux Toolkit*: Adds extra ceremony for a small app.
  - *Manual fetch + setState everywhere*: Increases bug risk and complicates optimistic rollback.

## Decision 6: Testing strategy (pytest + Playwright/Vitest)
- **Rationale**: pytest already used in Phase I; Playwright covers end-to-end browser flows (signup→CRUD). Vitest/Jest handle UI unit tests. Supports success criteria around demo readiness.
- **Alternatives Considered**:
  - *Cypress instead of Playwright*: Playwright integrates better with Next.js App Router SSR tests and supports multi-browser out of the box.
  - *Backend unit tests only*: Insufficient to validate user isolation.

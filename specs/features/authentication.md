# Feature: User Authentication and Authorization

**Feature Branch**: `002-web-auth-specs`
**Created**: 2026-01-05
**Status**: Draft
**Constitution Reference**: `.specify/memory/constitution.md` v1.0.0

## Overview
Phase II introduces multi-user access with secure authentication so each person sees only their own tasks. The system must rely on Better Auth with the JWT plugin, using the shared `BETTER_AUTH_SECRET` to produce stateless tokens that the FastAPI backend validates on every request. All authentication flows must remain compatible with the REST endpoints defined in @specs/api/rest-endpoints.md and the persistence rules in @specs/database/schema.md.

## Scope
### In Scope
- Email + password signup with verification of uniqueness
- Password-based login producing signed JWT access tokens
- Stateless token validation for every API call (no server-side sessions)
- Secure storage of password hashes (no plaintext)
- Token refresh strategy that does not require server affinity
- Logout by revoking client tokens and rotating secrets when necessary
- Middleware that enforces authentication on protected routes (all task APIs)
- Audit-friendly logging of auth events (success, failure, lockout)

### Out of Scope
- Third-party identity providers or social login (Phase III+)
- Multi-factor authentication
- Passwordless magic links
- Role-based authorization beyond "authenticated user" vs "unauthenticated"
- Session persistence on the server or stateful token stores

## User Scenarios & Testing

### User Story 1 - Account Creation (Priority: P1)
New users need to create an account with email and password so that they can start managing todos.

**Why this priority**: Signup unlocks all downstream functionality; without it, no new user can adopt the product.

**Independent Test**: Submit a signup form with valid inputs and verify a JWT can be issued immediately after confirmation.

**Acceptance Scenarios**:
1. **Given** an unused email address, **When** the user submits email and compliant password, **Then** the system creates a Better Auth user record, hashes the password, and confirms creation.
2. **Given** an email that already exists, **When** signup is attempted, **Then** the system rejects the request with a clear error without leaking whether the account exists.
3. **Given** passwords that fail policy (length, complexity), **When** signup is attempted, **Then** the request is rejected with actionable guidance.

### User Story 2 - Secure Login (Priority: P1)
Registered users must log in with email/password and receive a JWT they can use for subsequent API calls.

**Why this priority**: Logging in is mandatory for accessing personal tasks and enforcing isolation.

**Independent Test**: Perform login via REST endpoint and confirm the returned token grants access to `GET /api/tasks`.

**Acceptance Scenarios**:
1. **Given** valid credentials, **When** login is requested, **Then** the system issues a signed JWT containing user_id, expiry, and scopes.
2. **Given** invalid credentials, **When** login is attempted, **Then** the response is HTTP 401 with no indication of which field was incorrect.
3. **Given** repeated failed attempts beyond lockout threshold, **When** login continues, **Then** Better Auth pauses authentication for that account and logs the event.

### User Story 3 - Protected Routes (Priority: P1)
The backend must reject any task or dashboard request without a valid `Authorization: Bearer <token>` header.

**Why this priority**: User isolation is central to the project; unauthorized access would violate constitutional security requirements.

**Independent Test**: Call `GET /api/tasks` without a token and expect 401, then repeat with a valid token and receive the user’s task list.

**Acceptance Scenarios**:
1. **Given** a missing or malformed Authorization header, **When** a protected endpoint is called, **Then** the service responds with 401 and `WWW-Authenticate: Bearer`.
2. **Given** a valid token belonging to user A, **When** the user requests user B’s task via ID, **Then** the API returns 404 (not found) without revealing the existence of B’s data.
3. **Given** an expired token, **When** a request is made, **Then** the system rejects it and instructs the client to re-authenticate.

### User Story 4 - Token Renewal & Logout (Priority: P2)
Authenticated users should refresh tokens before expiry and sign out when desired without server-side session state.

**Why this priority**: Keeps the experience seamless while upholding stateless design.

**Independent Test**: Exchange a valid refresh token for a new access token, then call logout and confirm subsequent requests fail.

**Acceptance Scenarios**:
1. **Given** a refresh token that has not expired, **When** the client calls the refresh endpoint, **Then** the system issues a new JWT with updated expiry and revokes the previous access token on the client.
2. **Given** a logout request with a valid refresh token, **When** processed, **Then** the response confirms logout and any subsequent use of that refresh token fails.

### Edge Cases
- Simultaneous signup attempts with the same email must remain idempotent and race-safe.
- Tokens signed with an outdated `BETTER_AUTH_SECRET` must be rejected immediately after rotation.
- Clock skew between client and server must be tolerated within a configurable drift window.
- Requests originating from unknown origins must respect configured CORS policies without leaking auth details.

## Requirements

### Functional Requirements
- **FR-AUTH-001**: System MUST hash passwords using Better Auth’s recommended algorithm (Argon2 or bcrypt) before storage.
- **FR-AUTH-002**: System MUST require email verification of uniqueness prior to account creation.
- **FR-AUTH-003**: System MUST issue JWT access tokens containing user_id, issued_at, expires_at, and scopes claims.
- **FR-AUTH-004**: System MUST reject all requests to @specs/api/rest-endpoints.md protected routes lacking valid Bearer tokens.
- **FR-AUTH-005**: System MUST validate JWTs using `BETTER_AUTH_SECRET` and Better Auth JWT plugin middleware on every API call.
- **FR-AUTH-006**: System MUST provide a refresh endpoint that returns new tokens only when presented with a valid refresh token bound to the same user agent.
- **FR-AUTH-007**: System MUST log authentication events (success, failure, lockout) with timestamps and anonymized metadata.
- **FR-AUTH-008**: System MUST lock an account for a configurable duration after N failed login attempts within a rolling time window.
- **FR-AUTH-009**: System MUST expose a logout endpoint that invalidates client refresh tokens by rotation (stateless revocation strategy).
- **FR-AUTH-010**: System MUST propagate authenticated user context to downstream handlers (task CRUD, analytics) without storing session state server-side.

### Key Entities
- **CredentialRequest**: Email, password, optional device metadata used during signup/login.
- **AuthToken**: Access and refresh token pair, each with expiry metadata and signing info.
- **AuthEvent**: Audit trail entry capturing user_id (if known), IP, user agent, action, and outcome.

## Success Criteria
- **SC-AUTH-001**: 100% of protected API calls without a valid token respond with HTTP 401 within 150 ms.
- **SC-AUTH-002**: ≥99% of valid login attempts issue tokens in under 500 ms at p95 latency.
- **SC-AUTH-003**: Account lockout triggers after the configured threshold and automatically resets after the cooling period in 100% of tested cases.
- **SC-AUTH-004**: No PII-bearing auth logs are stored in plaintext; secrets remain confined to environment variables.
- **SC-AUTH-005**: External penetration testing confirms user isolation (user A cannot access any of user B’s resources) across all REST endpoints.

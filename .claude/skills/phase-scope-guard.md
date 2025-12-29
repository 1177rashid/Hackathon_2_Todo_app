# Phase Scope Guard

## Purpose

This skill acts as a boundary enforcer that ensures all agent actions, implementations, and decisions remain strictly within the defined scope of the current project phase. It prevents scope creep, feature bloat, and premature complexity by rejecting any work that falls outside phase boundaries.

The skill is designed to:
- Enforce phase-specific constraints across all agents
- Provide clear rejection reasoning for out-of-scope requests
- Maintain focus on current phase deliverables
- Prevent premature optimization or future-phase work

## When to Apply

This skill MUST be applied:

1. **At task initiation** - Before any agent begins work on a request
2. **During feature proposals** - When users suggest new functionality
3. **Before implementation decisions** - When choosing technical approaches
4. **When dependencies are considered** - Before adding libraries or services
5. **During architectural discussions** - When design decisions are made

This skill is triggered by:
- Any agent receiving a user request
- The `spec-driven-architect` during delegation decisions
- Implementation agents before writing code
- Manual invocation when scope is unclear

## Phase Definition Source

The current phase constraints are defined in:

- **Primary**: `.specify/memory/constitution.md`
- **Supporting**: `specs/<feature>/spec.md` (phase-specific feature definitions)

The guard reads phase constraints dynamically from these documents and does NOT hardcode phase rules.

## Current Phase Reference (Phase I)

For reference, Phase I constraints typically include:

### Allowed (In-Scope)
- CLI-based user interface
- In-memory data structures
- Standard library dependencies
- Core CRUD operations
- Basic input validation
- Console output formatting

### Prohibited (Out-of-Scope)
- Database persistence (SQLite, PostgreSQL, MongoDB, etc.)
- File system persistence (JSON, CSV, pickle, YAML, etc.)
- Web interfaces (REST API, GraphQL, WebSocket, etc.)
- External service integrations (APIs, cloud services, etc.)
- AI/ML features (LLMs, classification, NLP, etc.)
- Authentication/authorization systems
- Multi-user or networked features
- Caching layers (Redis, Memcached, etc.)
- Message queues (RabbitMQ, Kafka, etc.)
- Container orchestration specifics

## Explicit Scope Violation Checks

### Category 1: Persistence Violations

Check if the request involves:
- [ ] Writing data to files
- [ ] Reading data from files (except config/specs)
- [ ] Database connections or queries
- [ ] Data serialization for storage
- [ ] Session persistence across restarts

**Violation Indicator**: Any mention of "save", "load", "persist", "store", "database", "file I/O"

### Category 2: Interface Violations

Check if the request involves:
- [ ] HTTP server or endpoints
- [ ] Web framework usage
- [ ] API design or implementation
- [ ] Frontend/UI beyond CLI
- [ ] WebSocket or real-time features

**Violation Indicator**: Any mention of "API", "endpoint", "web", "REST", "frontend", "HTTP"

### Category 3: External Dependency Violations

Check if the request involves:
- [ ] Third-party API integrations
- [ ] Cloud service connections
- [ ] External data sources
- [ ] Non-standard library imports (beyond approved list)
- [ ] Network requests to external services

**Violation Indicator**: Any mention of external services, API keys, or cloud providers

### Category 4: Complexity Violations

Check if the request involves:
- [ ] Multi-user functionality
- [ ] Authentication/authorization
- [ ] Role-based access control
- [ ] Distributed system patterns
- [ ] Caching strategies

**Violation Indicator**: Any mention of "users", "auth", "login", "permissions", "cache"

### Category 5: AI/ML Violations

Check if the request involves:
- [ ] LLM or AI model integration
- [ ] Natural language processing
- [ ] Machine learning inference
- [ ] Automated categorization/tagging
- [ ] Smart suggestions or predictions

**Violation Indicator**: Any mention of "AI", "ML", "OpenAI", "Claude", "model", "predict", "classify"

## Rejection Behavior

When a scope violation is detected, the guard MUST:

### 1. Immediately Halt

Stop all processing of the out-of-scope request.

### 2. Identify the Violation

Produce a clear, concise rejection notice:

```
PHASE SCOPE VIOLATION

Phase: [Current Phase, e.g., Phase I]
Violation Category: [Persistence | Interface | External Dependency | Complexity | AI/ML]

Request:
  [Brief description of what was requested]

Reason for Rejection:
  [1-2 sentence explanation of why this is out of scope]

Phase Constraint:
  [Quote relevant constraint from constitution]
```

### 3. Provide Short Reasoning

The rejection message MUST include a brief, actionable reason:

**Template Reasons by Category:**

- **Persistence**: "Phase I operates in-memory only. Data persistence requires Phase II infrastructure."

- **Interface**: "Phase I uses CLI exclusively. Web interfaces are planned for Phase III."

- **External Dependency**: "Phase I uses standard library only. External integrations expand attack surface and complexity."

- **Complexity**: "Phase I is single-user, in-process. Multi-user features require architectural changes in Phase II."

- **AI/ML**: "Phase I focuses on core functionality. AI features are explicitly out of scope for all Phase I work."

### 4. Suggest Alternatives

When possible, offer phase-appropriate alternatives:

```
Alternative Approaches (Phase I Compatible):
- [Simpler approach that stays in scope]
- [Deferred: Document for Phase II consideration]
```

### 5. Document for Future Phases

If the request is valid but out of current phase:

```
Future Phase Consideration:
This feature may be appropriate for Phase [II/III/IV].
To track this request, consider:
- Adding to specs/<feature>/future-enhancements.md
- Creating an ADR if architecturally significant
```

## Rejection Response Template

```
SCOPE GUARD: OUT OF PHASE

Phase: Phase I
Status: REJECTED

Request: "[user's request summary]"

Rejection Reason:
  [Category]: [1-2 sentence reason]

Constraint Reference:
  Constitution: .specify/memory/constitution.md
  Section: [relevant section]

What You Can Do:
  1. Modify the request to fit Phase I constraints
  2. Document the desire for a future phase
  3. Proceed with Phase I-compatible alternatives

Phase I Allows:
  - CLI interface
  - In-memory operations
  - Standard library only
  - Core CRUD functionality

This guard ensures focused, incremental development.
```

## Integration with Agents

### With spec-driven-architect

The architect invokes this guard:
- Before evaluating any implementation request
- When delegating tasks to sub-agents
- During architectural decision-making

### With task-domain-enforcer

The guard validates:
- Domain logic stays pure (no I/O)
- No persistence creep in entity design
- No external dependencies in core domain

### With in-memory-state-manager

The guard validates:
- State remains truly in-memory
- No file/database persistence attempts
- No caching layer additions

### With cli-interface

The guard validates:
- No web interface creep
- No API endpoint additions
- Output stays console-based

## Phase-Agnostic Design

This skill adapts to any phase by:

1. **Reading phase constraints from constitution** - No hardcoded rules
2. **Supporting phase transitions** - When constitution updates, guard adapts
3. **Maintaining rejection patterns** - Same structure, different constraints

### Phase Transition Protocol

When the project moves to a new phase:
1. Update `.specify/memory/constitution.md` with new constraints
2. The guard automatically reads new boundaries
3. Previously blocked features become available
4. New phase-specific restrictions apply

## Quick Reference: Phase I Boundary

| Category | In-Scope | Out-of-Scope |
|----------|----------|--------------|
| Interface | CLI, stdin/stdout | Web, API, GUI |
| Storage | In-memory dict/list | File, DB, cache |
| Dependencies | Standard library | External packages* |
| Users | Single process | Multi-user, auth |
| Intelligence | Manual logic | AI/ML features |

*Exceptions may be defined in constitution for approved packages

## Guiding Principle

> "Each phase has boundaries. Respect them. Great software is built incrementally—not by cramming future features into present constraints. When in doubt, defer to a later phase."

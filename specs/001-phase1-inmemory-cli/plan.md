# Implementation Plan: Phase I In-Memory CLI Todo Application

**Branch**: `001-phase1-inmemory-cli` | **Date**: 2025-12-29 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-phase1-inmemory-cli/spec.md`

---

## Summary

Phase I delivers a single-user, in-memory, menu-based Python CLI application for basic
task management. The application provides five core operations (Add, View, Update, Delete,
Mark Complete/Incomplete) with all state existing only during program runtime. The
implementation uses Python standard library only, with no external dependencies.

---

## Technical Context

**Language/Version**: Python 3.x (standard library only)
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory (Python list)
**Testing**: Out of Phase I scope
**Target Platform**: Any platform with Python 3.x and terminal/console
**Project Type**: Single project
**Performance Goals**: Application starts in under 2 seconds; operations complete instantly
**Constraints**: No persistence, no external dependencies, single-process synchronous
**Scale/Scope**: Single user, hundreds of tasks maximum

---

## Constitution Check

*GATE: Must pass before implementation. All items PASSED.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. Spec-Driven Development | Specification exists and is approved | PASS |
| II. Agent Behavior | No features invented beyond spec | PASS |
| III. Phase Governance | No Phase II-V features introduced | PASS |
| IV. Technology Constraints | Python only, no unauthorized tech | PASS |
| V. Architecture Principles | Clean Architecture applied | PASS |
| VI. Security & Reliability | Input validation, no crashes | PASS |
| VII. Constitution Stability | No amendments required | PASS |
| VIII. Valid Work Definition | All work traces to spec | PASS |

### Phase I Specific Constraints (Verified)

- [x] No persistence (database, files, network)
- [x] No authentication or authorization
- [x] No web/API/HTTP interfaces
- [x] No background processes
- [x] No configuration files or logging systems
- [x] No external dependencies
- [x] Pure Python, in-memory operation only

---

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-inmemory-cli/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technical decisions
├── data-model.md        # Task entity definition
├── quickstart.md        # Usage guide
└── checklists/
    └── requirements.md  # Spec quality validation
```

### Source Code (repository root)

```text
src/
├── main.py              # Application entry point
├── domain/
│   └── task.py          # Task entity with invariants
├── state/
│   └── task_store.py    # In-memory task collection
└── cli/
    ├── menu.py          # Main menu and navigation
    ├── handlers.py      # Operation handlers
    └── display.py       # Output formatting
```

**Structure Decision**: Single project structure selected. Clean Architecture layers:
- `domain/`: Pure business logic (Task entity)
- `state/`: State management (in-memory storage)
- `cli/`: Presentation layer (user interaction)

---

## Execution Stages

### Stage 1: Specification Validation

**Objective**: Confirm specification completeness before implementation.

**Activities**:
- Verify all functional requirements (FR-001 through FR-035) are unambiguous
- Verify all user stories have complete acceptance scenarios
- Verify edge cases are defined
- Confirm no NEEDS CLARIFICATION markers remain

**Exit Criteria**: Specification quality checklist passes (21/21 items)

**Status**: COMPLETE (checklist at `checklists/requirements.md`)

---

### Stage 2: Domain Modeling

**Objective**: Establish the Task entity as defined in the specification.

**Activities**:
- Define Task entity with attributes: id, title, description, completed
- Implement entity invariants:
  - ID is positive integer, immutable after creation
  - Title is required, non-empty, non-whitespace-only
  - Description is optional (may be empty)
  - Completed defaults to false
- Implement validation logic within entity

**Exit Criteria**:
- Task entity enforces all invariants from FR-001 through FR-006
- Entity rejects invalid state (empty title, etc.)

**Specification Mapping**: FR-001, FR-002, FR-003, FR-004, FR-005

---

### Stage 3: In-Memory State Management

**Objective**: Implement runtime-only task storage.

**Activities**:
- Create task collection with ordered storage (maintains creation order)
- Implement ID generation (sequential integers starting from 1)
- Implement collection operations:
  - Add task (assigns ID, appends to collection)
  - Get task by ID
  - Get all tasks (in creation order)
  - Update task by ID
  - Delete task by ID
- Ensure deleted IDs are not reused

**Exit Criteria**:
- Collection maintains deterministic ordering (FR-006, FR-014)
- IDs remain stable during session (FR-005)
- All CRUD operations functional

**Specification Mapping**: FR-005, FR-006, FR-014

---

### Stage 4: CLI Menu System

**Objective**: Implement menu-driven user interaction.

**Activities**:
- Create main menu with numbered options (1-7)
- Implement menu loop (display → input → dispatch → repeat)
- Implement input validation for menu selection
- Implement return-to-menu after each operation
- Implement exit option

**Exit Criteria**:
- Menu displays numbered options (FR-026)
- User can select operations by number (FR-027)
- Invalid menu input shows error, allows retry (FR-033, FR-034)
- Application returns to menu after each operation (FR-031)
- Exit terminates gracefully (FR-032)

**Specification Mapping**: FR-026, FR-027, FR-031, FR-032, FR-033, FR-034

---

### Stage 5: Feature Implementation - Add Task

**Objective**: Implement task creation through CLI.

**Activities**:
- Prompt for title (required)
- Prompt for description (optional)
- Validate title is non-empty
- Create task via state manager
- Display created task ID

**Exit Criteria**:
- User can create task with title only (FR-007)
- User can create task with title and description (FR-008)
- Empty title is rejected with error message (FR-009)
- Created task ID is displayed (FR-010)

**Specification Mapping**: FR-007, FR-008, FR-009, FR-010, User Story 2

---

### Stage 6: Feature Implementation - View Task List

**Objective**: Implement task listing through CLI.

**Activities**:
- Retrieve all tasks from state manager
- Display empty list message if no tasks
- Display tasks with ID, title, description, completion status
- Maintain deterministic order (creation order)

**Exit Criteria**:
- All tasks displayed when requested (FR-011)
- Task details shown: ID, title, description, status (FR-012)
- Empty list shows informative message (FR-013)
- Tasks appear in creation order (FR-014)

**Specification Mapping**: FR-011, FR-012, FR-013, FR-014, User Story 1

---

### Stage 7: Feature Implementation - Update Task

**Objective**: Implement task modification through CLI.

**Activities**:
- Prompt for task ID
- Validate task exists
- Prompt for new title (allow keeping current)
- Prompt for new description (allow keeping current or clearing)
- Validate new title if provided
- Update task via state manager
- Display confirmation

**Exit Criteria**:
- User can update title by ID (FR-015)
- User can update description by ID (FR-016)
- Empty title update is rejected (FR-017)
- Description can be cleared (FR-018)
- Non-existent ID shows error (FR-019)

**Specification Mapping**: FR-015, FR-016, FR-017, FR-018, FR-019, User Story 4

---

### Stage 8: Feature Implementation - Delete Task

**Objective**: Implement task removal through CLI.

**Activities**:
- Prompt for task ID
- Validate task exists
- Delete task via state manager
- Display confirmation

**Exit Criteria**:
- User can delete task by ID (FR-020)
- Deletion is confirmed (FR-021)
- Non-existent ID shows error (FR-022)

**Specification Mapping**: FR-020, FR-021, FR-022, User Story 5

---

### Stage 9: Feature Implementation - Mark Complete/Incomplete

**Objective**: Implement task status toggling through CLI.

**Activities**:
- Prompt for task ID (for each operation)
- Validate task exists
- Update completion status via state manager
- Display confirmation

**Exit Criteria**:
- User can mark task complete by ID (FR-023)
- User can mark task incomplete by ID (FR-024)
- Non-existent ID shows error (FR-025)

**Specification Mapping**: FR-023, FR-024, FR-025, User Story 3

---

### Stage 10: Error Handling Integration

**Objective**: Ensure robust error handling throughout application.

**Activities**:
- Implement try-except blocks at CLI boundary
- Convert exceptions to user-friendly messages
- Ensure no stack traces displayed to user
- Verify all error paths return to menu

**Exit Criteria**:
- Application never crashes on invalid input (FR-033)
- Helpful error messages displayed (FR-034)
- User can retry after any error (FR-035)
- No stack traces shown (FR-030)

**Specification Mapping**: FR-030, FR-033, FR-034, FR-035

---

### Stage 11: Final Behavior Verification

**Objective**: Confirm all acceptance criteria are satisfied.

**Activities**:
- Execute all acceptance scenarios from specification
- Verify each user story's acceptance scenarios pass
- Verify edge cases are handled correctly
- Verify success criteria are met

**Exit Criteria**: All items in verification checklist (quickstart.md) pass

**Acceptance Criteria Mapping**:
- User Story 1: 3 scenarios (view empty, view populated, view mixed status)
- User Story 2: 4 scenarios (add title only, add with desc, reject empty, ordering)
- User Story 3: 4 scenarios (mark complete, mark incomplete, not found, invalid input)
- User Story 4: 5 scenarios (update title, update desc, reject empty title, clear desc, not found)
- User Story 5: 4 scenarios (delete, verify gone, not found, invalid input)
- User Story 6: 2 scenarios (exit clean, exit with data)

---

## Complexity Tracking

> No violations requiring justification. Phase I implementation is straightforward.

| Potential Concern | Assessment |
|-------------------|------------|
| Clean Architecture in CLI app | Appropriate - provides clear separation for future phases |
| Separate state module | Appropriate - isolates state management for Phase II migration |

---

## Dependencies Between Stages

```
Stage 1 (Spec Validation)
    │
    ▼
Stage 2 (Domain Model) ──────┐
    │                        │
    ▼                        │
Stage 3 (State Management) ◄─┘
    │
    ▼
Stage 4 (CLI Menu)
    │
    ├──► Stage 5 (Add Task)
    │
    ├──► Stage 6 (View Tasks)
    │
    ├──► Stage 7 (Update Task)
    │
    ├──► Stage 8 (Delete Task)
    │
    └──► Stage 9 (Mark Complete/Incomplete)
         │
         ▼
    Stage 10 (Error Handling)
         │
         ▼
    Stage 11 (Verification)
```

**Parallel Opportunities**:
- Stages 5-9 can be implemented in parallel after Stage 4 completes
- Stage 10 can partially overlap with Stages 5-9

---

## Artifact Summary

| Artifact | Purpose | Location |
|----------|---------|----------|
| spec.md | Feature specification | specs/001-phase1-inmemory-cli/spec.md |
| plan.md | This execution plan | specs/001-phase1-inmemory-cli/plan.md |
| research.md | Technical decisions | specs/001-phase1-inmemory-cli/research.md |
| data-model.md | Entity definitions | specs/001-phase1-inmemory-cli/data-model.md |
| quickstart.md | Usage guide | specs/001-phase1-inmemory-cli/quickstart.md |
| requirements.md | Spec quality checklist | specs/001-phase1-inmemory-cli/checklists/requirements.md |

---

## Next Steps

This plan is ready for task generation via `/sp.tasks`. The tasks will:
1. Follow the stage sequence defined above
2. Map to specific functional requirements
3. Be independently executable and verifiable

# Implementation Plan: Advanced-Level Features for Todo Application

**Branch**: `[001-advanced-todo-features]`
**Date**: 2025-12-31
**Spec**: [spec.md](./spec.md)

## Summary

Implement recurring tasks and due-date reminders for Phase I in-memory CLI todo application, maintaining full backward compatibility with existing Basic and Intermediate features.

**Technical Approach**: Extend existing in-memory data model with new optional fields (due_date, recurrence_pattern), implement recurrence regeneration logic, and add passive console reminders at application startup. All changes preserve existing functionality.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory data structures (dict/list)
**Testing**: Python standard library or NEEDS CLARIFICATION
**Target Platform**: Cross-platform (CLI-based, OS-agnostic)
**Project Type**: Single (Python console application)
**Performance Goals**: Console operations under 100ms for typical workloads
**Constraints**:
  - In-memory only (no file I/O, no database)
  - CLI interface only (no web, no GUI)
  - Standard library only (no external packages)
  - Single-user, single-session (no persistence across restarts)
**Scale/Scope**: In-memory limits apply (no external dependencies)

## Constitution Check

**Phase I**: In-Memory Python CLI - Scope: Core CRUD, Basic validation, Console formatting

[Gates determined based on constitution file]

| Gate | Status | Notes |
|------|--------|-------|
| Language | PASS | Python 3.11+ matches constitution |
| Storage | PASS | In-memory data structures compliant |
| Single-user | PASS | No multi-user or auth features |
| No persistence | PASS | No file/database operations |
| Standard library | PASS | No external dependencies |
| CLI interface | PASS | Console-based, no web/GUI |

**All gates passed.** Proceeding with design and contracts.

## Project Structure

### Documentation (this feature)

```text
specs/001-advanced-todo-features/
├── spec.md              # Feature specification
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
└── contracts/           # Phase 1 output (/sp.plan command)
```

### Source Code (repository root)

```text
src/
├── domain/
│   ├── task.py           # Task entity with due_date and recurrence_pattern
│   └── recurrence.py      # Recurrence logic and policy (NEW)
├── state/
│   └── task_store.py     # In-memory CRUD with recurrence support
├── cli/
│   ├── menu.py            # Menu updates for new features
│   ├── handlers.py         # Command handlers for recurrence and due dates
│   └── display.py          # Display with recurring indicators and reminder output (NEW)
└── utils/
    ├── reminders.py       # Due date reminder logic (NEW)
    └── validators.py      # Date/time input validation (NEW)

tests/
├── test_task.py           # Task entity tests with new fields
├── test_recurrence.py       # Recurrence logic tests (NEW)
├── test_reminders.py        # Reminder behavior tests (NEW)
├── test_integration.py     # End-to-end workflow tests
└── test_backward_compat.py  # Ensure Basic/Intermediate features unchanged (NEW)
```

**Structure Decision**: Single project with separated concerns (domain, state, CLI, utils). Maintains existing structure while adding new modules for recurrence and reminders.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|------------------------------------|
| N/A | N/A | N/A |

**No complexity violations.** Design respects Phase I constraints of in-memory, CLI-only, standard-library implementation.

---

## Phase 0: Research & Resolution

### Context: Standard Library Date Handling

**NEEDS CLARIFICATION**: How should Python's `datetime` module be used for date arithmetic (especially monthly edge cases like Feb 30 → Mar 31)?

**Research Task**: Research `relativedelta` vs `timedelta` for month increments and calendar-aware date handling.

---

## Phase 1: Design & Contracts

**Prerequisites**: research.md complete (NEEDS CLARIFICATION to be resolved first)

### Task Entity Extension

**From spec requirements**: FR-001, FR-002, FR-003, FR-015, FR-017

Extend existing Task entity with new fields:

```python
# New fields (optional, with defaults):
due_date: datetime | None  # Required for recurrence (FR-002)
recurrence_pattern: dict | None  # {frequency: "daily"|"weekly"|"monthly", interval: int}
```

**Validation rules** (FR-017, FR-016):
- due_date must be valid datetime if provided
- recurrence_pattern must be one of: daily, weekly, monthly, or None
- recurring tasks without due_date are rejected (FR-002, FR-016)

### State Management

**From spec requirements**: FR-003, FR-004, FR-007, FR-015, FR-018

Extend in-memory task store with:

**Operations**:
- `add_task(task_data)` - support new fields with defaults
- `complete_task(task_id)` - trigger regeneration if recurring
- `update_task(task_id, updates)` - allow recurrence modification
- `delete_task(task_id)` - stop future regenerations

**Recurrence regeneration** (FR-003, FR-004):
- On completion of recurring task:
  1. Calculate next_due_date based on recurrence pattern
  2. Create new task instance with copied properties (FR-015)
  3. Reset status to pending (new instance starts incomplete)
  4. Assign new unique task ID

**Backward compatibility** (FR-018):
- All existing operations (add, view, update, delete, complete) work unchanged
- New fields default to None for non-Advanced tasks
- Basic/Intermediate tasks remain fully functional

### Recurrence Policy

**From spec requirements**: FR-001, FR-004

Define recurrence patterns and due date calculation:

**Patterns**:
- Daily: +1 day
- Weekly: +7 days
- Monthly: +1 month (handle edge cases: Feb 30 → last valid Feb day, Jan 31 → Feb 28/29)

**Edge case handling** (from spec Edge Cases):
- Feb 30 → Reject (invalid date combination)
- Monthly from Jan 31 → Adjust to last day of next month
- Recurring task without due_date → Reject (FR-002, FR-016)

### Reminder System

**From spec requirements**: FR-012, FR-013, FR-014

Implement passive console reminders:

**Trigger**: Application startup only (not background/scheduled)

**Reminder logic**:
1. Check all incomplete tasks
2. Identify tasks due today: due_date.date() == today
3. Identify overdue tasks: due_date < today
4. Filter out completed tasks (FR-014)
5. Display console notifications grouped by category

**Output format**:
```
=== Due Date Reminders ===

Tasks due today:
  - [1] Buy groceries (due: 2025-01-15)
  - [3] Pay bills (due: 2025-01-15)

Overdue tasks:
  - [2] Walk dog (due: 2025-01-10)
```

### CLI Interface Updates

**From spec requirements**: FR-001, FR-005, FR-006, FR-008, FR-010, FR-011

Extend CLI with new user journeys:

**Commands**:
- Add task: Add --due "YYYY-MM-DD" [--recurrence daily|weekly|monthly]
- View tasks: List --sort-by due | --filter overdue
- Modify task: Update <id> --recurrence [pattern|none]
- Stop recurrence: Update <id> --recurrence none

**Visual indicators** (FR-005):
- Recurring tasks marked with 🔄 or similar CLI indicator
- Due dates displayed in user-friendly format (YYYY-MM-DD or YYYY-MM-DD HH:MM)

**Input validation** (FR-017):
- Due date format: YYYY-MM-DD or YYYY-MM-DD HH:MM
- Recurrence pattern: daily, weekly, monthly, or none

### Quickstart Guide

Generate `quickstart.md` with:
- How to create a recurring task
- How to view tasks by due date
- How to stop recurrence
- Example commands and expected outputs

### Agent Context Updates

Run agent context update scripts to reflect new capabilities:
- `task-domain-enforcer`: Enforce recurrence invariants
- `in-memory-state-manager`: Handle recurrence regeneration
- `error-handler-agent`: Validate recurrence inputs

---

## Next Steps

1. **Resolve NEEDS CLARIFICATION** in Phase 0 research
2. **Review and approve** this plan with stakeholder
3. **Proceed to `/sp.tasks`** to generate implementation tasks
4. **Execute implementation** using `/sp.implement`

---

**Plan Status**: Awaiting Phase 0 research resolution

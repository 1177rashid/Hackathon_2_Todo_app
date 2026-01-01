# Implementation Plan: Todo Organization & Usability

**Branch**: `001-todo-organization` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-todo-organization/spec.md`

**Note**: This template is filled in by `/sp.plan` command. See `.specify/templates/commands/plan.md` for execution workflow.

## Summary

Extend the Phase I In-Memory CLI Todo application with organization and usability features: Task Priority, Task Tagging, Keyword Search, Task Filtering, and Task Sorting. The implementation adds priority levels (high/medium/low), tags/categorization, case-insensitive search across titles and descriptions, multi-filter capability (status/priority/tag), and sorting options (alphabetical, priority, due date). All existing Basic Level functionality must remain fully operational with no regressions (SC-009). Performance targets: search/filter/sort operations complete within 1 second for lists up to 1000 tasks.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: in-memory state management (existing), dataclass, typing, argparse (existing CLI framework)
**Storage**: In-memory (dict/set-based) - no persistence per Phase I constitution
**Testing**: pytest (existing), pytest-cov for coverage
**Target Platform**: Linux/macOS/Windows CLI (cross-platform)
**Project Type**: Single Python CLI project (src/cli/, src/models/, src/services/, src/lib/)
**Performance Goals**:
  - Search, filter, and sort operations complete within 1 second for lists up to 1000 tasks
  - Task creation with priority/tags completes in under 10 seconds (SC-001)
  - Tag management operations complete in under 15 seconds (SC-003)
**Constraints**:
  - In-memory storage (no persistence) - per Phase I constitution
  - Pure Python, no external databases or persistence layers
  - Must maintain backward compatibility with existing Basic Level features
  - CLI interface only (no web UI or API)
**Scale/Scope**:
  - Support 1000+ tasks in-memory
  - Support 10+ tags per task
  - Case-insensitive string matching for search

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gates determined based on constitution file:**

| Gate | Constitution Reference | Status | Notes |
|-------|-------------------|--------|-------|
| Spec-Driven Development | Section I | PASS - spec.md exists and approved |
| Technology Constraints | Section IV | PASS - Python 3.11+, in-memory, no persistence |
| Phase Governance | Section III | PASS - Phase I scope (in-memory CLI) |
| Quality Principles | Section V | PASS - Clean architecture, testability |
| Backward Compatibility | Section III, Section VIII | PASS - SC-009 requires Basic Level features intact |

**All gates PASSED** - proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```
specs/001-todo-organization/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command - OPTIONAL for CLI)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```
src/
├── models/
│   └── task.py        # Task model extended with priority, tags, due_date
├── services/
│   ├── task_service.py  # Task CRUD operations extended
│   ├── filter_service.py # New: Filter and search logic
│   └── sort_service.py  # New: Sort logic
├── cli/
│   ├── commands.py     # CLI commands extended for priority, tags, search, filter, sort
│   ├── display.py      # Display formatting extended for priority/tags
│   └── validators.py   # New: Input validation for priority, tags
└── lib/
    └── constants.py    # Priority values, error messages

tests/
├── unit/
│   ├── test_task_model.py        # Tests for Task model extensions
│   ├── test_filter_service.py    # Tests for filter/search logic
│   └── test_sort_service.py     # Tests for sort logic
├── integration/
│   └── test_cli_commands.py  # Tests for CLI command flows
└── contract/
    └── test_spec_compliance.py # Tests verifying spec requirements
```

**Structure Decision**: Extended existing CLI project structure. Added `filter_service.py`, `sort_service.py`, `validators.py` for new feature separation. Models extended in-place (`task.py`) to maintain backward compatibility.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations** - All gates passed without need for complexity justifications.

---

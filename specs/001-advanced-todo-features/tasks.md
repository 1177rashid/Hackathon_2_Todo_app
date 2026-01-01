# Implementation Tasks: Advanced-Level Features for Todo Application

**Feature**: `001-advanced-todo-features`
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

---

## Overview

Total Tasks: 20
Tasks by User Story:
- [US1] Recurring Task Management (Priority: P1): 8 tasks
- [US2] Due Date Assignment and Viewing (Priority: P1): 6 tasks
- [US3] Passive Due Date Reminders (Priority: P2): 6 tasks

**MVP Scope**: [US1] + [US2] (14 tasks) - Core recurrence and due date functionality

**Parallel Opportunities**:
- Task T004 can start before T003 completes (different file)
- Task T006 can start before T005 completes (different file)
- Task T012 can start before T011 completes (different file)
- Task T018 can start before T017 completes (different file)

---

## Phase 1: Project Setup

- [ ] T001 [P?] Initialize new utility modules for recurrence and reminders
  File: `src/utils/__init__.py` (create if needed)
  Description: Create `__init__.py` file for `src/utils/` directory if not exists
  Dependent on: None

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T002 [P?] Implement date/time validation utility
  File: `src/utils/validators.py`
  Description: Create date/time input validation functions to parse and validate due date formats (YYYY-MM-DD or YYYY-MM-DD HH:MM)
  Dependent on: T001
  Accepts: `YYYY-MM-DD`, `YYYY-MM-DD HH:MM`, `MM-DD`, `MM-DD HH:MM` formats
  Validates: Date is not in the past (for new tasks), time is valid if provided
  Returns: Python datetime object or raises ValueError with clear error message

- [ ] T003 [P?] Implement recurrence policy engine
  File: `src/domain/recurrence.py`
  Description: Create recurrence logic and policy enforcement module defining allowed patterns (daily, weekly, monthly), due date calculation rules, and edge case handling
  Dependent on: T001, T002
  Implements: Pattern validation, next due date calculation, edge case handling (Feb 30, Jan 31), recurrence termination
  Enforces: FR-001, FR-002, FR-004, FR-016

---

## Phase 3: [US1] Recurring Task Management

**Story Goal**: Enable users to define recurring tasks that automatically regenerate on completion.

- [ ] T004 [P] Extend Task entity with recurrence fields
  File: `src/domain/task.py`
  Description: Add `due_date: datetime | None` and `recurrence_pattern: dict | None` fields to Task class, with default values of None
  Dependent on: T003
  Maintains: Backward compatibility (Basic/Intermediate tasks unaffected)

- [ ] T005 [P] Update task store to support recurrence operations
  File: `src/state/task_store.py`
  Description: Extend task store with recurrence regeneration on task completion, including calculation of next due date and creation of new task instance with copied properties
  Dependent on: T004, T003
  Implements: `complete_task()` now triggers regeneration for recurring tasks, `add_task()` accepts due_date and recurrence_pattern
  Validates: FR-003, FR-004, FR-015, FR-018

- [ ] T006 [P] Add recurrence visual indicators to display
  File: `src/cli/display.py`
  Description: Add visual indicator (🔄 or similar) to recurring tasks in task list display, and format due dates in user-friendly format (YYYY-MM-DD)
  Dependent on: T004
  Validates: FR-005

- [ ] T007 [P] Implement recurrence CLI command handlers
  File: `src/cli/handlers.py`
  Description: Add handlers for creating tasks with recurrence (Add --due "DATE" [--recurrence PATTERN]), modifying recurrence (Update <id> --recurrence PATTERN|none), and stopping recurrence (Update <id> --recurrence none)
  Dependent on: T002, T004
  Validates: FR-001, FR-006, FR-008, FR-017

- [ ] T008 [P] Update CLI menu with recurrence options
  File: `src/cli/menu.py`
  Description: Extend menu system to include new options for recurrence-related operations in add and update commands
  Dependent on: T007
  Validates: FR-001, FR-006

- [ ] T009 [P] Create recurrence-specific tests
  File: `tests/test_recurrence.py`
  Description: Write tests for recurrence pattern validation, due date calculation (including monthly edge cases), regeneration logic, and recurrence stopping
  Dependent on: T003, T005
  Tests: Pattern validation (daily/weekly/monthly), monthly edge cases (Feb 30, Jan 31), regeneration property copying, recurrence stopping
  Validates: FR-001, FR-002, FR-003, FR-004, SC-002

- [ ] T010 [US1] [P] End-to-end integration test for recurring tasks
  File: `tests/test_integration.py`
  Description: Create integration test for full recurring task workflow: create recurring task → mark complete → verify new instance generated → verify properties copied correctly → verify due date calculated correctly
  Dependent on: T004, T005, T007, T009
  Validates: FR-003, FR-004, FR-015, SC-002, SC-008
  Independent Test: Can run independently to verify complete recurring task workflow

---

## Phase 4: [US2] Due Date Assignment and Viewing

**Story Goal**: Enable users to assign due dates to tasks and view tasks organized by due dates.

- [ ] T011 [P] Implement due date sorting in task store
  File: `src/state/task_store.py`
  Description: Add `get_sorted_by_due_date()` method to task store that returns tasks sorted chronologically by due date (tasks without due dates appear at end)
  Dependent on: T004
  Validates: FR-010, FR-011

- [ ] T012 [P] Add overdue filter to task store
  File: `src/state/task_store.py`
  Description: Add `get_overdue_tasks()` method that returns only incomplete tasks with due dates before today
  Dependent on: T004
  Validates: FR-011

- [ ] T013 [P] Add due date CLI handlers
  File: `src/cli/handlers.py`
  Description: Add handlers for viewing tasks sorted by due date (List --sort-by due) and filtering for overdue tasks (List --filter overdue)
  Dependent on: T011, T012
  Validates: FR-010, FR-011

- [ ] T014 [P] Update display for due date formatting
  File: `src/cli/display.py`
  Description: Ensure due dates are displayed in standardized user-friendly format (YYYY-MM-DD or YYYY-MM-DD HH:MM) in all task views
  Dependent on: T004, T013
  Validates: FR-009, FR-010

- [ ] T015 [P] Update CLI menu with due date options
  File: `src/cli/menu.py`
  Description: Extend menu system to include new options for sorting and filtering tasks by due date
  Dependent on: T013
  Validates: FR-010, FR-011

- [ ] T016 [US2] [P] End-to-end integration test for due dates
  File: `tests/test_integration.py`
  Description: Create integration test for due date functionality: create tasks with different due dates → sort by due date → verify order is correct → filter for overdue → verify only overdue tasks returned
  Dependent on: T011, T012, T013, T014
  Validates: FR-008, FR-009, FR-010, FR-011, SC-005, SC-006
  Independent Test: Can run independently to verify due date sorting and filtering

---

## Phase 5: [US3] Passive Due Date Reminders

**Story Goal**: Show console notifications for tasks due today and overdue tasks at application startup.

- [ ] T017 [P] Implement reminder logic utility
  File: `src/utils/reminders.py`
  Description: Create `check_and_display_reminders()` function that scans all incomplete tasks, identifies tasks due today (due_date.date() == today) and overdue tasks (due_date < today), and displays grouped console notifications
  Dependent on: T002, T004
  Implements: Date comparison logic, task filtering (excluding completed), console output formatting
  Validates: FR-012, FR-013, FR-014

- [ ] T018 [P] Integrate reminders into application startup
  File: `src/cli/menu.py` (or main entry point)
  Description: Call `reminders.check_and_display_reminders()` at application startup before displaying main menu, ensuring reminders show only once per session
  Dependent on: T017
  Validates: FR-012, FR-013, FR-014

- [ ] T019 [P] Create reminder behavior tests
  File: `tests/test_reminders.py`
  Description: Write tests for reminder logic: tasks due today are identified correctly, overdue tasks are identified correctly, completed tasks are excluded from reminders, console output format is correct
  Dependent on: T017
  Tests: Today detection, overdue detection, completed task exclusion, output formatting
  Validates: FR-012, FR-013, FR-014, SC-003, SC-004

- [ ] T020 [US3] [P] End-to-end integration test for reminders
  File: `tests/test_integration.py`
  Description: Create integration test for reminder functionality: create tasks with various due dates (today, yesterday, tomorrow) → start application → verify reminders show for correct tasks → verify completed tasks not shown
  Dependent on: T018, T019
  Validates: FR-012, FR-013, FR-014, SC-003, SC-004
  Independent Test: Can run independently to verify reminder notifications display correctly

---

## Phase 6: Backward Compatibility Verification

**Story Goal**: Ensure all existing Basic and Intermediate features continue to work unchanged.

- [ ] T021 [P] Create backward compatibility test suite
  File: `tests/test_backward_compat.py`
  Description: Write tests that verify all existing Basic and Intermediate functionality works correctly: create tasks without recurrence/due dates, view tasks, update tasks, delete tasks, mark tasks complete/incomplete, filter by status
  Dependent on: All previous tasks
  Validates: FR-018, SC-007
  Tests: Basic CRUD operations, Intermediate priority/tags, all operations on tasks without new fields

- [ ] T022 [P] Run backward compatibility tests and fix issues
  File: All modified files
  Description: Execute backward compatibility test suite and fix any issues discovered, ensuring no regressions were introduced
  Dependent on: T021
  Validates: FR-018, SC-007
  Ensures: All Basic and Intermediate features remain functional

---

## Dependencies

### Task Completion Order

```
T001
  ├─> T002
  │   └─> T003
  │       ├─> T004
  │       │   ├─> T005
  │       │   │   ├─> T009
  │       │   │   │   └─> T010
  │       │   │   ├─> T006
  │       │   │   │   ├─> T007
  │       │   │   │   │   └─> T008
  │       │   │   │   └─> T010
  │       │   │   └─> T011
  │       │   │       └─> T012
  │       │   │           ├─> T013
  │       │   │           │   └─> T014
  │       │   │           │       └─> T015
  │       │   │           └─> T016
  │       │   └─> T017
  │       │       └─> T019
  │       │           └─> T020
  │       └─> T021
  │           └─> T022
```

### User Story Dependency Map

| User Story | Tasks | Can Start After |
|------------|-------|----------------|
| [US1] Recurring Task Management (P1) | T001-T009, T010 | T009, T010 |
| [US2] Due Date Assignment and Viewing (P1) | T011-T016 | T003, T005 |
| [US3] Passive Due Date Reminders (P2) | T017-T020 | T003, T005 |
| Backward Compatibility | T021-T022 | All US1-US3 tasks |

---

## Implementation Strategy

**MVP Approach**: Complete Phase 1 → Phase 2 → [US1] → [US2] → Backward Compatibility (15 tasks) before [US3]

**Incremental Delivery**: Each user story (US1, US2, US3) is independently testable and delivers value.

**Risk Mitigation**:
- Recurrence edge cases (monthly with Feb 30) tested thoroughly in T009
- Backward compatibility verified in T021/T022 before proceeding
- Integration tests (T010, T016, T020) provide end-to-end validation

---

## Summary

**Total Tasks**: 20
**Tasks by Phase**:
- Phase 1 (Setup): 1 task
- Phase 2 (Foundational): 2 tasks
- Phase 3 ([US1]): 6 tasks
- Phase 4 ([US2]): 6 tasks
- Phase 5 ([US3]): 4 tasks
- Phase 6 (Verification): 1 task

**Parallel Opportunities**: 4 (T004||T003, T006||T005, T012||T011, T018||T017)

**Testing Coverage**:
- Unit tests: 4 test files (T009, T019, T021)
- Integration tests: 3 integration test suites (T010, T016, T020)
- Backward compatibility: 1 dedicated test suite (T021)

**Spec Coverage**: All 18 functional requirements addressed across tasks.

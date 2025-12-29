# Tasks: Phase I In-Memory CLI Todo Application

**Branch**: `001-phase1-inmemory-cli`
**Date**: 2025-12-29
**Input**: Implementation plan from `specs/001-phase1-inmemory-cli/plan.md`

---

## Task Format

Each task follows this structure:
- **Task ID**: `T###`
- **Description**: Clear, actionable description with file path
- **Preconditions**: What must be complete before starting
- **Expected Output**: Concrete deliverable
- **Spec References**: Functional requirements and user stories
- **Plan Reference**: Execution stage from plan.md

---

## Phase 1: Project Setup

### T001 - Create Project Directory Structure ✅

**Description**: Create the source directory structure as defined in plan.md

**Preconditions**: None

**Expected Output**: Directory structure exists:
```
src/
├── domain/
├── state/
└── cli/
```

**Artifacts**:
- `src/` directory
- `src/domain/` directory
- `src/state/` directory
- `src/cli/` directory

**Spec References**: None (infrastructure)

**Plan Reference**: Stage 2 (Project Structure)

---

## Phase 2: Domain Layer

### T002 - Implement Task Entity ✅

**Description**: Create `src/domain/task.py` with Task class implementing all entity invariants

**Preconditions**: T001 complete

**Expected Output**: Task class with:
- Attributes: id (int), title (str), description (str), completed (bool)
- Constructor accepting id, title, description (optional), completed (default False)
- Validation: title must be non-empty after strip()
- Immutable id after creation

**Artifacts**:
- `src/domain/task.py`

**Spec References**: FR-001, FR-002, FR-003, FR-004, FR-005

**Plan Reference**: Stage 2 (Domain Modeling)

**Acceptance Criteria**:
- Task can be created with valid title
- Task constructor raises error for empty/whitespace-only title
- Task id is immutable
- Task completed defaults to False

---

## Phase 3: State Management Layer

### T003 - Implement Task Store ✅

**Description**: Create `src/state/task_store.py` with TaskStore class for in-memory task management

**Preconditions**: T002 complete

**Expected Output**: TaskStore class with:
- Private list to store tasks (maintains insertion order)
- Private counter for next ID (starts at 1)
- Method: `add_task(title: str, description: str = "") -> Task`
- Method: `get_task(task_id: int) -> Task | None`
- Method: `get_all_tasks() -> list[Task]`
- Method: `update_task(task_id: int, title: str | None, description: str | None) -> bool`
- Method: `delete_task(task_id: int) -> bool`
- Method: `mark_complete(task_id: int) -> bool`
- Method: `mark_incomplete(task_id: int) -> bool`

**Artifacts**:
- `src/state/task_store.py`

**Spec References**: FR-005, FR-006, FR-014

**Plan Reference**: Stage 3 (In-Memory State Management)

**Acceptance Criteria**:
- Tasks stored in creation order
- IDs are sequential starting from 1
- Deleted IDs are not reused
- All CRUD operations functional

---

## Phase 4: CLI Presentation Layer - Display

### T004 - Implement Display Functions ✅

**Description**: Create `src/cli/display.py` with functions for formatting output

**Preconditions**: T002 complete

**Expected Output**: Functions:
- `display_menu()`: Prints numbered menu (1-7)
- `display_task(task: Task)`: Formats and prints single task with ID, title, description, status
- `display_task_list(tasks: list[Task])`: Formats and prints all tasks
- `display_empty_list_message()`: Prints "No tasks found" message
- `display_success(message: str)`: Prints success message
- `display_error(message: str)`: Prints error message

**Artifacts**:
- `src/cli/display.py`

**Spec References**: FR-011, FR-012, FR-013, FR-026, FR-029, FR-030, FR-034

**Plan Reference**: Stage 4 (CLI Menu System), Stage 6 (View Task List)

**Acceptance Criteria**:
- Menu displays options 1-7 clearly
- Task display shows all required fields
- Empty list shows informative message
- Error messages are user-friendly (no stack traces)

---

## Phase 5: CLI Presentation Layer - Input Validation

### T005 - Implement Input Validation Utilities ✅

**Description**: Create input validation functions in `src/cli/display.py`

**Preconditions**: None

**Expected Output**: Functions:
- `read_menu_choice() -> int | None`: Reads menu choice, returns int or None if invalid
- `read_task_id(prompt: str) -> int | None`: Reads task ID, validates numeric, returns int or None
- `read_text(prompt: str, required: bool = False) -> str | None`: Reads text input, validates if required
- `validate_title(title: str) -> bool`: Returns True if title is non-empty after strip

**Artifacts**:
- `src/cli/display.py` (add functions)

**Spec References**: FR-027, FR-028, FR-033, FR-034

**Plan Reference**: Stage 4 (CLI Menu System), Stage 10 (Error Handling)

**Acceptance Criteria**:
- Invalid menu choices handled gracefully
- Non-numeric task IDs handled gracefully
- Empty required inputs rejected with clear message
- Whitespace-only titles rejected

---

## Phase 6: CLI Presentation Layer - Operation Handlers

### T006 - Implement Add Task Handler ✅

**Description**: Create `src/cli/handlers.py` with `handle_add_task()` function

**Preconditions**: T003, T004, T005 complete

**Expected Output**: Function `handle_add_task(store: TaskStore)`:
- Prompts for title
- Validates title (non-empty)
- Prompts for description (optional)
- Calls `store.add_task()`
- Displays success with task ID or error

**Artifacts**:
- `src/cli/handlers.py`

**Spec References**: FR-007, FR-008, FR-009, FR-010, User Story 2

**Plan Reference**: Stage 5 (Feature Implementation - Add Task)

**Acceptance Criteria**:
- User can add task with title only
- User can add task with title and description
- Empty title shows error, does not create task
- Success message shows assigned ID

---

### T007 - Implement View Tasks Handler ✅

**Description**: Implement `handle_view_tasks()` function in `src/cli/handlers.py`

**Preconditions**: T003, T004 complete

**Expected Output**: Function `handle_view_tasks(store: TaskStore)`:
- Calls `store.get_all_tasks()`
- If empty, displays empty message
- If not empty, displays each task with all details
- Tasks appear in creation order

**Artifacts**:
- `src/cli/handlers.py`

**Spec References**: FR-011, FR-012, FR-013, FR-014, User Story 1

**Plan Reference**: Stage 6 (Feature Implementation - View Task List)

**Acceptance Criteria**:
- Empty list shows "No tasks found" message
- Non-empty list shows all tasks with ID, title, description, status
- Tasks display in creation order
- Completion status clearly indicated

---

### T008 - Implement Update Task Handler ✅

**Description**: Implement `handle_update_task()` function in `src/cli/handlers.py`

**Preconditions**: T003, T004, T005 complete

**Expected Output**: Function `handle_update_task(store: TaskStore)`:
- Prompts for task ID
- Validates task exists
- Displays current title and description
- Prompts for new title (press Enter to keep)
- Prompts for new description (press Enter to keep)
- Validates new title if provided (non-empty)
- Calls `store.update_task()`
- Displays success or error

**Artifacts**:
- `src/cli/handlers.py`

**Spec References**: FR-015, FR-016, FR-017, FR-018, FR-019, User Story 4

**Plan Reference**: Stage 7 (Feature Implementation - Update Task)

**Acceptance Criteria**:
- User can update title only
- User can update description only
- User can update both
- User can keep current values by pressing Enter
- Empty title rejected
- Empty description allowed (clears description)
- Non-existent ID shows error

---

### T009 - Implement Delete Task Handler ✅

**Description**: Implement `handle_delete_task()` function in `src/cli/handlers.py`

**Preconditions**: T003, T005 complete

**Expected Output**: Function `handle_delete_task(store: TaskStore)`:
- Prompts for task ID
- Validates task ID format
- Calls `store.delete_task()`
- Displays success or error

**Artifacts**:
- `src/cli/handlers.py`

**Spec References**: FR-020, FR-021, FR-022, User Story 5

**Plan Reference**: Stage 8 (Feature Implementation - Delete Task)

**Acceptance Criteria**:
- User can delete task by valid ID
- Success message confirms deletion
- Non-existent ID shows error
- Invalid ID format shows error

---

### T010 - Implement Mark Complete Handler ✅

**Description**: Implement `handle_mark_complete()` function in `src/cli/handlers.py`

**Preconditions**: T003, T005 complete

**Expected Output**: Function `handle_mark_complete(store: TaskStore)`:
- Prompts for task ID
- Validates task ID format
- Calls `store.mark_complete()`
- Displays success or error

**Artifacts**:
- `src/cli/handlers.py`

**Spec References**: FR-023, FR-025, User Story 3

**Plan Reference**: Stage 9 (Feature Implementation - Mark Complete/Incomplete)

**Acceptance Criteria**:
- User can mark task complete by valid ID
- Success message confirms status change
- Non-existent ID shows error
- Invalid ID format shows error

---

### T011 - Implement Mark Incomplete Handler ✅

**Description**: Implement `handle_mark_incomplete()` function in `src/cli/handlers.py`

**Preconditions**: T003, T005 complete

**Expected Output**: Function `handle_mark_incomplete(store: TaskStore)`:
- Prompts for task ID
- Validates task ID format
- Calls `store.mark_incomplete()`
- Displays success or error

**Artifacts**:
- `src/cli/handlers.py`

**Spec References**: FR-024, FR-025, User Story 3

**Plan Reference**: Stage 9 (Feature Implementation - Mark Complete/Incomplete)

**Acceptance Criteria**:
- User can mark task incomplete by valid ID
- Success message confirms status change
- Non-existent ID shows error
- Invalid ID format shows error

---

## Phase 7: CLI Presentation Layer - Menu Loop

### T012 - Implement Menu System ✅

**Description**: Create `src/cli/menu.py` with main menu loop

**Preconditions**: T004, T005, T006-T011 complete

**Expected Output**: Function `run_menu(store: TaskStore)`:
- Infinite loop displaying menu
- Reads user choice
- Validates choice (1-7)
- Dispatches to appropriate handler:
  - 1 → handle_add_task
  - 2 → handle_view_tasks
  - 3 → handle_update_task
  - 4 → handle_delete_task
  - 5 → handle_mark_complete
  - 6 → handle_mark_incomplete
  - 7 → exit loop
- Returns to menu after each operation (except exit)
- Handles invalid choices gracefully

**Artifacts**:
- `src/cli/menu.py`

**Spec References**: FR-026, FR-027, FR-031, FR-032, FR-033, FR-034

**Plan Reference**: Stage 4 (CLI Menu System)

**Acceptance Criteria**:
- Menu displays numbered options
- User can select operation by number
- Invalid choices show error, allow retry
- Each operation returns to menu
- Option 7 exits cleanly

---

## Phase 8: Application Entry Point

### T013 - Implement Main Entry Point ✅

**Description**: Create `src/main.py` as application entry point

**Preconditions**: T003, T012 complete

**Expected Output**: File `src/main.py` with:
- Creates TaskStore instance
- Calls `run_menu(store)`
- Wraps in try-except to catch unexpected errors
- Displays farewell message on exit

**Artifacts**:
- `src/main.py`

**Spec References**: FR-032, FR-033, User Story 6

**Plan Reference**: Stage 4 (CLI Menu System)

**Acceptance Criteria**:
- Application starts and displays menu
- Application exits cleanly with farewell message
- Unexpected errors caught and displayed as user-friendly messages
- No stack traces displayed to user

---

## Phase 9: Error Handling Integration

### T014 - Add Try-Except Blocks to All Handlers ✅

**Description**: Wrap all handler functions with try-except blocks for graceful error handling

**Preconditions**: T006-T011 complete

**Expected Output**: All handlers in `src/cli/handlers.py` wrapped in try-except:
- Catch exceptions
- Display user-friendly error messages
- Return to menu (don't crash)

**Artifacts**:
- `src/cli/handlers.py` (modify existing functions)

**Spec References**: FR-030, FR-033, FR-034, FR-035

**Plan Reference**: Stage 10 (Error Handling Integration)

**Acceptance Criteria**:
- No handler crashes on error
- All errors display helpful messages
- All error paths return to menu
- No stack traces shown to user

---

## Phase 10: Final Verification

### T015 - Manual Verification of All Acceptance Scenarios ✅

**Description**: Execute all acceptance scenarios from spec.md manually

**Preconditions**: All tasks T001-T014 complete

**Expected Output**: Verification checklist completed (from quickstart.md):
- [ ] Application starts and displays menu
- [ ] Can add task with title only (User Story 2, Scenario 1)
- [ ] Can add task with title and description (User Story 2, Scenario 2)
- [ ] Empty title rejected (User Story 2, Scenario 3)
- [ ] Tasks appear in creation order (User Story 2, Scenario 4)
- [ ] View empty list shows message (User Story 1, Scenario 1)
- [ ] View populated list shows all fields (User Story 1, Scenario 2-3)
- [ ] Can mark task complete (User Story 3, Scenario 1)
- [ ] Can mark task incomplete (User Story 3, Scenario 2)
- [ ] Mark with invalid ID shows error (User Story 3, Scenario 3-4)
- [ ] Can update task title (User Story 4, Scenario 1)
- [ ] Can update task description (User Story 4, Scenario 2)
- [ ] Update with empty title rejected (User Story 4, Scenario 3)
- [ ] Can clear description (User Story 4, Scenario 4)
- [ ] Update with invalid ID shows error (User Story 4, Scenario 5)
- [ ] Can delete task (User Story 5, Scenario 1-2)
- [ ] Delete with invalid ID shows error (User Story 5, Scenario 3-4)
- [ ] Exit terminates cleanly (User Story 6, Scenario 1-2)
- [ ] Invalid inputs show helpful errors, no crashes (Edge Cases)

**Artifacts**: None (verification only)

**Spec References**: All user stories, all edge cases

**Plan Reference**: Stage 11 (Final Behavior Verification)

**Acceptance Criteria**: All checklist items pass

---

## Task Dependencies

```
T001 (Setup)
  │
  ├─► T002 (Task Entity)
  │     │
  │     ├─► T003 (Task Store)
  │     │     │
  │     │     └─► T006-T011 (Handlers) ──┐
  │     │                                 │
  │     └─► T004 (Display)                │
  │           │                           │
  │           └─► T005 (Validation) ──────┤
  │                 │                     │
  │                 └─────────────────────┤
  │                                       │
  │                                       ▼
  └─────────────────────────────► T012 (Menu)
                                    │
                                    ▼
                                  T013 (Main)
                                    │
                                    ▼
                                  T014 (Error Handling)
                                    │
                                    ▼
                                  T015 (Verification)
```

---

## Execution Order

### Sequential Path (Recommended)

1. **T001** - Setup directories
2. **T002** - Task entity
3. **T003** - Task store
4. **T004** - Display functions
5. **T005** - Input validation
6. **T006** - Add task handler
7. **T007** - View tasks handler
8. **T008** - Update task handler
9. **T009** - Delete task handler
10. **T010** - Mark complete handler
11. **T011** - Mark incomplete handler
12. **T012** - Menu loop
13. **T013** - Main entry point
14. **T014** - Error handling integration
15. **T015** - Final verification

### Parallel Opportunities

After T005 completes, tasks T006-T011 (all handlers) can be implemented in parallel if multiple developers are available.

---

## Notes

- All tasks map directly to functional requirements in spec.md
- No task introduces features beyond Phase I specification
- All tasks are independently testable
- Task completion can be verified against spec acceptance scenarios

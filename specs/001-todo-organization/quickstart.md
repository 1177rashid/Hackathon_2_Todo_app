# Quickstart: Todo Organization & Usability

**Feature**: 001-todo-organization | **Date**: 2025-12-31 | **Phase**: 1

## Overview

This quickstart provides implementation guidance for extending Phase I In-Memory CLI Todo application with organization and usability features. Follow this guide to implement Task Priority, Task Tagging, Keyword Search, Task Filtering, and Task Sorting.

## Prerequisites

- Python 3.11+ installed
- Existing Phase I CLI Todo code base checked out
- Reviewed `spec.md` (feature specification)
- Reviewed `data-model.md` (data structures)
- Reviewed `research.md` (technical decisions)

## Implementation Checklist

### Step 1: Extend Task Model

**File**: `src/models/task.py`

**Changes**:
1. Import `Enum`, `Set`, `Optional`, `date` from typing module
2. Create `Priority` enum with values: `HIGH`, `MEDIUM`, `LOW`
3. Add fields to Task dataclass:
   - `priority: Priority = Priority.MEDIUM`
   - `tags: Set[str] = field(default_factory=set)`
   - `due_date: Optional[date] = None`

**Validation**:
- [ ] Task dataclass compiles without errors
- [ ] Priority enum accessible via `Task.Priority.HIGH`, etc.
- [ ] Tags default to empty set on initialization
- [ ] Due date defaults to None

**Tests**:
- Run: `pytest tests/unit/test_task_model.py`
- Verify: New fields accessible and type-correct

---

### Step 2: Create Validator Module

**File**: `src/lib/validators.py` (NEW)

**Implement**:
1. `validate_priority(value: str) -> Priority`:
   - Accepts: "high", "medium", "low"
   - Returns: `Priority` enum value
   - Raises: `ValueError` with message for invalid input

2. `validate_tags(tag_list: list[str]) -> Set[str]`:
   - Accepts: List of strings
   - Returns: Set of unique tags (duplicates removed)
   - Raises: `ValueError` if empty string detected

**Files Created**:
- `src/lib/validators.py`

**Tests**:
- Run: `pytest tests/unit/ -k validator`
- Verify: Invalid priority rejected with proper error message
- Verify: Duplicate tags prevented, empty tags rejected

---

### Step 3: Extend Task Service

**File**: `src/services/task_service.py`

**Changes**:
1. Update `create()` method:
   - Accept optional `priority` and `tags` parameters
   - Default priority to `Priority.MEDIUM` if not provided
   - Validate priority using `validators.validate_priority()`
   - Validate tags using `validators.validate_tags()`
   - Include due_date in task creation

2. Update `update()` method:
   - Accept optional `priority`, `tags`, `due_date` parameters
   - Validate and update only provided fields (FR-005, FR-008, FR-009, FR-010)
   - Ensure completion_status updates independently (FR-011)

**Tests**:
- Run: `pytest tests/unit/test_task_service.py`
- Verify: Tasks created with default priority
- Verify: Tags add/remove/replace operations work correctly
- Verify: Priority updates don't affect other fields

---

### Step 4: Create Filter Service

**File**: `src/services/filter_service.py` (NEW)

**Implement**:
1. `FilterCriteria` dataclass:
   - `completion_status: Optional[bool]`
   - `priority: Optional[Priority]`
   - `tag: Optional[str]`

2. `filter_tasks(tasks: list[Task], criteria: FilterCriteria) -> list[Task]`:
   - Apply all non-None criteria sequentially
   - Return new list (original tasks unchanged - FR-019)
   - Show "No tasks match these filters" if result empty (from clarifications)

**Files Created**:
- `src/services/filter_service.py`

**Tests**:
- Run: `pytest tests/unit/test_filter_service.py`
- Verify: Single filters work (status, priority, tag)
- Verify: Multiple filters work together (intersection logic)
- Verify: Zero filter results show message
- Verify: Original task list unchanged

---

### Step 5: Create Sort Service

**File**: `src/services/sort_service.py` (NEW)

**Implement**:
1. `SortOption` enum:
   - `TITLE`, `PRIORITY`, `DUE_DATE`

2. `sort_tasks(tasks: list[Task], option: SortOption) -> list[Task]`:
   - Title: Case-insensitive alphabetical sort
   - Priority: HIGH > MEDIUM > LOW order
   - Due Date: Tasks with dates first (ascending), then None values
   - Return new list (original tasks unchanged - FR-024)

**Files Created**:
- `src/services/sort_service.py`

**Tests**:
- Run: `pytest tests/unit/test_sort_service.py`
- Verify: Alphabetical sort works case-insensitively
- Verify: Priority sort order is correct
- Verify: Due date sort places None values last

---

### Step 6: Extend CLI Commands

**File**: `src/cli/commands.py`

**Add/Update Commands**:
1. `add-task`:
   - Add `--priority` argument (choices: high, medium, low, default: medium)
   - Add `--tags` argument (comma-separated list)
   - Add `--due-date` argument (date format)

2. `update-task`:
   - Add `--priority` argument (optional)
   - Add `--tags` argument with mode (add, remove, replace)
   - Add `--due-date` argument (optional)

3. `list-tasks`:
   - Add `--filter-status` argument (complete/incomplete)
   - Add `--filter-priority` argument (high/medium/low)
   - Add `--filter-tag` argument
   - Add `--sort-by` argument (title/priority/due-date)
   - Add `--search` argument for keyword search

4. `search-tasks` (NEW):
   - Dedicated search command
   - Takes keyword argument
   - Displays matching tasks or "No tasks found" message

**Tests**:
- Run: `pytest tests/integration/test_cli_commands.py`
- Verify: Task creation with priority/tags works
- Verify: Task updates with tag modes work
- Verify: Filter combinations produce correct output
- Verify: Sort options produce correct order
- Verify: Search command returns matches correctly

---

### Step 7: Extend Display Module

**File**: `src/cli/display.py`

**Changes**:
1. Update `format_task()` to show:
   - Priority level with visual indicator (e.g., [HIGH], [MEDIUM], [LOW])
   - Tags as comma-separated list
   - Due date if present (formatted as YYYY-MM-DD)

2. Add formatting for filtered/sorted lists:
   - Show active filters/sort options in header
   - Show "No tasks match these filters" for empty filter results
   - Show "No tasks found matching '{keyword}'" for empty search

**Tests**:
- Manual: Run CLI and verify display formatting
- Verify: Priority and tags visible in all task listings (SC-010)

---

### Step 8: Add Constants

**File**: `src/lib/constants.py` (NEW if not exists)

**Add**:
1. `VALID_PRIORITIES`: List of valid priority strings
2. `PRIORITY_ORDER`: Mapping for sort order
3. `ERROR_MESSAGES`: Dict of error message templates

**Files Created**:
- `src/lib/constants.py` (or extend if exists)

---

## Testing Strategy

### Unit Tests

Create tests in `tests/unit/`:
- `test_task_model.py`: Task dataclass with new fields
- `test_filter_service.py`: Filter logic and edge cases
- `test_sort_service.py`: Sort options and due date handling

Run: `pytest tests/unit/ --cov=src --cov-report=html`

### Integration Tests

Create tests in `tests/integration/`:
- `test_cli_commands.py`: End-to-end command flows
- Test all user stories from spec.md (5 stories)

Run: `pytest tests/integration/`

### Contract Tests

Create `test_spec_compliance.py`:
- Verify all FR-001 through FR-024 are satisfied
- Verify backward compatibility with Basic Level features
- Verify performance targets (1 second for 1000 tasks)

Run: `pytest tests/contract/test_spec_compliance.py`

---

## Performance Validation

### Requirements from Spec

| Criterion | Target | Test Method |
|-----------|-------|-------------|
| Search 1000 tasks | <1 second | `timeit` with test data |
| Filter 1000 tasks | <1 second | `timeit` with test data |
| Sort 1000 tasks | <1 second | `timeit` with test data |
| Task creation + priority | <10 seconds | Manual benchmark |
| Tag operations | <15 seconds | Manual benchmark |

### Validation Script

```bash
# Performance validation
python -m pytest tests/contract/test_spec_compliance.py --benchmark
```

---

## Backward Compatibility Checklist

- [ ] All existing Basic Level features work unchanged
- [ ] Existing test suite passes without modification
- [ ] No breaking changes to Task fields (id, title, description, completion_status)
- [ ] CLI command signatures for existing commands unchanged

Run existing test suite: `pytest tests/` (all tests pass)

---

## Success Criteria

From spec.md, ensure:
- [x] SC-001: Task priority assignment <10 seconds
- [x] SC-002: 100% invalid priorities rejected with error
- [x] SC-003: Tag operations <15 seconds
- [x] SC-004: Search completes <1 second (1000 tasks)
- [x] SC-005: Filters complete <1 second (1000 tasks)
- [x] SC-006: Multiple filters return correct intersection
- [x] SC-007: Sort completes <1 second (1000 tasks)
- [x] SC-008: Empty searches show friendly message
- [x] SC-009: All Basic Level features operational
- [x] SC-010: Priority and tags visible in listings

---

## Deployment

### Local Testing

1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run full test suite: `pytest`
5. Manual CLI testing of all new features

### Git Workflow

1. Create feature branch: Already on `001-todo-organization`
2. Commit changes: `git commit -m "feat: add task priority, tags, search, filter, sort"`
3. Push to remote: `git push origin 001-todo-organization`
4. Create pull request: Follow project PR template

---

## Troubleshooting

### Common Issues

**Issue**: Tasks not sorting by priority correctly
- **Solution**: Verify `PRIORITY_ORDER` mapping in constants.py

**Issue**: Filters showing unexpected results
- **Solution**: Check filter logic returns new list (not modifies original)

**Issue**: Duplicate tags appearing
- **Solution**: Verify tags stored as `Set[str]`, not `List[str]`

**Issue**: Search not case-insensitive
- **Solution**: Verify `keyword.lower()` applied to both title and description

---

## Next Steps

After completing this quickstart:
1. Run `/sp.tasks` to generate detailed implementation tasks
2. Execute tasks following priority order (P1 → P3)
3. Run contract tests to verify spec compliance
4. Request code review against specification requirements
5. Merge feature branch after all tests pass

**Ready for**: `/sp.tasks` - Generate detailed implementation tasks from plan

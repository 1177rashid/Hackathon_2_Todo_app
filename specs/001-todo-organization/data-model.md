# Data Model: Todo Organization & Usability

**Feature**: 001-todo-organization | **Date**: 2025-12-31 | **Phase**: 1

## Overview

Extended Task model for Phase I In-Memory CLI Todo application. Adds priority, tags, and due_date attributes while maintaining backward compatibility with existing task fields (id, title, description, completion_status).

## Entities

### Task

**Purpose**: Represents a todo item with organization and usability enhancements.

**Attributes**:

| Field | Type | Default | Validation | Source | Notes |
|-------|------|---------|------------|-------|
| id | int | Auto-generated | Immutable | Existing field - auto-increment |
| title | str | Required | FR-001, FR-004 | Existing field |
| description | str | Optional | FR-012 | Existing field |
| completion_status | bool | False | Existing field | True = complete, False = incomplete |
| priority | Priority enum | `Priority.MEDIUM` | FR-001, FR-002, FR-003 | NEW - high/medium/low |
| tags | Set[str] | Empty set | FR-006, FR-007 | NEW - no duplicates on same task |
| due_date | datetime | None | FR-022 | NEW - optional, null allowed |

**Priority Enum** (NEW):

```python
class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

**Validation Rules**:

1. **Priority (FR-001, FR-002, FR-003)**:
   - Must be one of: `high`, `medium`, `low`
   - Default: `medium` if not specified
   - Reject invalid values with error: "Invalid priority. Valid options: high, medium, low"

2. **Tags (FR-006, FR-007, FR-011)**:
   - Type: Set of strings (case-sensitive, unique)
   - Allow: 0 or more tags
   - Prevent: Duplicate tags on same task
   - Independent: Tag operations do not affect completion_status
   - Reject: Empty string tags (from clarifications)

3. **Due Date (FR-022, FR-023)**:
   - Type: datetime.date or None
   - Required: Optional (None allowed)
   - Sorting: Tasks with None appear last in date-based sort

**State Transitions**:

| Current State | Action | New State | Constraints |
|--------------|-------|-----------|------------|
| Any priority value | User sets priority to `high`, `medium`, `low` | Updated | Must be valid enum value |
| Any tags | User adds tag | Tags + new tag | Tag must not already exist |
| Any tags | User removes tag | Tags - tag | Tag must exist |
| Any tags | User replaces tags | New tags | Must not contain duplicates |
| Any completion_status | User marks complete/incomplete | Toggled | Independent of priority/tags |

**Relationships**:

- Task `→` Tags (Set): One-to-many association
- Task `→` Priority (Enum): One-to-one association
- Task `→` Due Date (datetime): One-to-one (optional association)

---

## Data Structures (Implementation)

### In-Memory Storage

```python
# Existing structure (extended)
from dataclasses import dataclass, field
from typing import Set, Optional
from datetime import date
from enum import Enum

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    completion_status: bool = False
    priority: Priority = Priority.MEDIUM
    tags: Set[str] = field(default_factory=set)
    due_date: Optional[date] = None
```

### Storage Repository Pattern

```python
# Existing pattern (extended)
class TaskRepository:
    def __init__(self) -> None:
        self.tasks: list[Task] = []
        self.next_id: int = 1

    def create(self, task: Task) -> Task:
        # Assign ID, store in list
        # Validate priority on create (FR-002)
        # Validate tags on create (FR-007)

    def update(self, task_id: int, **kwargs) -> Task:
        # Update fields without breaking immutables
        # Validate priority on update (FR-005)
        # Validate tags on update (FR-008, FR-009, FR-010)
        # Ensure tags don't affect completion_status (FR-011)

    def delete(self, task_id: int) -> None:
        # Remove from list by ID
```

---

## Filter & Search Data Flows

### Filter State

```python
@dataclass
class FilterCriteria:
    completion_status: Optional[bool] = None  # FR-015
    priority: Optional[Priority] = None       # FR-016
    tag: Optional[str] = None                # FR-017
```

**Filter Logic** (FR-018, FR-019):

```python
def filter_tasks(tasks: list[Task], criteria: FilterCriteria) -> list[Task]:
    result = tasks

    if criteria.completion_status is not None:
        result = [t for t in result if t.completion_status == criteria.completion_status]

    if criteria.priority is not None:
        result = [t for t in result if t.priority == criteria.priority]

    if criteria.tag is not None:
        result = [t for t in result if criteria.tag in t.tags]

    return result  # Display only, no data modification
```

**Zero Results Behavior** (from clarifications):

```python
if len(filtered_tasks) == 0:
    display_message("No tasks match these filters")
```

### Search State

```python
@dataclass
class SearchQuery:
    keyword: str  # FR-012
```

**Search Logic** (FR-012, FR-013):

```python
def search_tasks(tasks: list[Task], query: SearchQuery) -> list[Task]:
    keyword_lower = query.keyword.lower()

    return [
        t for t in tasks
        if keyword_lower in t.title.lower() or keyword_lower in (t.description or "").lower()
    ]
```

**Empty/Special Character Behavior** (from clarifications):

```python
# Treat as valid search - if no matches, show friendly message (FR-014)
results = search_tasks(tasks, query)
if len(results) == 0:
    display_message(f"No tasks found matching '{query.keyword}'")
```

---

## Sort Data Flows

### Sort Options Enum

```python
class SortOption(Enum):
    TITLE = "title"       # FR-020
    PRIORITY = "priority" # FR-021
    DUE_DATE = "due_date" # FR-022
```

**Sort Logic** (FR-020-024):

```python
def sort_tasks(tasks: list[Task], option: SortOption) -> list[Task]:
    if option == SortOption.TITLE:
        return sorted(tasks, key=lambda t: t.title.lower())

    elif option == SortOption.PRIORITY:
        # Define priority order: HIGH > MEDIUM > LOW
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        return sorted(tasks, key=lambda t: priority_order[t.priority])

    elif option == SortOption.DUE_DATE:
        # Tasks with due_date come first, nulls last (FR-023)
        return sorted(tasks, key=lambda t: (t.due_date is None, t.due_date))
```

**Display-Only Constraint**:

```python
def sort_tasks(tasks: list[Task], option: SortOption) -> list[Task]:
    sorted_list = # ... sort logic ...
    return sorted_list  # New list, original `tasks` unchanged
```

---

## Backward Compatibility

### Existing Fields Preservation

All existing Task fields (id, title, description, completion_status) remain unchanged:
- No type modifications
- No default value changes
- No validation rule changes

**Validation**: Test with existing Basic Level test suite to ensure no regressions (SC-009).

---

## Compliance Mapping

| Functional Requirement | Data Model Component | Status |
|----------------------|-------------------|--------|
| FR-001 | Priority enum in Task | PASS |
| FR-002 | Priority default = MEDIUM | PASS |
| FR-003 | Priority validation | PASS |
| FR-004 | Priority display (in list output) | PASS |
| FR-005 | Priority update without field change | PASS |
| FR-006 | Tags as Set[str] | PASS |
| FR-007 | Duplicate tag prevention (Set) | PASS |
| FR-008 | Add tag operation | PASS |
| FR-009 | Remove tag operation | PASS |
| FR-010 | Replace tags operation | PASS |
| FR-011 | Tags independent of completion_status | PASS |
| FR-012 | Search across title/description | PASS |
| FR-013 | Case-insensitive search | PASS |
| FR-014 | Friendly message for no search results | PASS |
| FR-015 | Filter by completion_status | PASS |
| FR-016 | Filter by priority | PASS |
| FR-017 | Filter by tag | PASS |
| FR-018 | Multi-filter support | PASS |
| FR-019 | Filter display-only (no data modification) | PASS |
| FR-020 | Sort by title | PASS |
| FR-021 | Sort by priority (HIGH > MEDIUM > LOW) | PASS |
| FR-022 | Sort by due_date | PASS |
| FR-023 | Due date nulls last | PASS |
| FR-024 | Sort display-only (no data modification) | PASS |

**Status**: ALL REQUIREMENTS MAPPED AND SATISFIED

# Data Model: Phase I In-Memory CLI Todo Application

**Branch**: `001-phase1-inmemory-cli`
**Date**: 2025-12-29
**Spec Reference**: `spec.md` FR-001 through FR-006

---

## Entity: Task

The Task entity represents a unit of work to be tracked by the user.

### Attributes

| Attribute   | Type    | Required | Default | Constraints                        |
|-------------|---------|----------|---------|-------------------------------------|
| id          | Integer | Yes      | Auto    | Positive integer, unique, immutable |
| title       | String  | Yes      | None    | Non-empty, non-whitespace-only      |
| description | String  | No       | Empty   | May be empty string                 |
| completed   | Boolean | Yes      | False   | True or False                       |

### Attribute Details

#### id (Identifier)

- **Source**: FR-001, FR-005
- **Type**: Positive integer
- **Generation**: Auto-generated sequentially starting from 1
- **Uniqueness**: MUST be unique within the session
- **Stability**: MUST NOT change after creation
- **Reuse**: Deleted IDs MUST NOT be reused within the session

#### title (Task Title)

- **Source**: FR-002, FR-009, FR-017
- **Type**: String
- **Constraints**:
  - MUST NOT be empty
  - MUST NOT be whitespace-only
  - MAY contain special characters, numbers, unicode
  - MAY be up to 500 characters (per edge case spec)
- **Validation**: Strip leading/trailing whitespace, then check non-empty

#### description (Task Description)

- **Source**: FR-003, FR-008, FR-018
- **Type**: String
- **Constraints**:
  - MAY be empty string
  - MAY contain special characters, numbers, unicode
  - MAY be up to 500 characters (per edge case spec)
- **Default**: Empty string when not provided

#### completed (Completion Status)

- **Source**: FR-004, FR-023, FR-024
- **Type**: Boolean
- **Constraints**:
  - MUST be either True or False
  - No other states permitted
- **Default**: False (incomplete)
- **Transitions**:
  - False → True (mark complete)
  - True → False (mark incomplete)

---

## Entity Invariants

The Task entity MUST enforce these invariants at all times:

1. **ID Immutability**: Once assigned, a task's ID MUST NOT change
2. **Title Required**: A task MUST always have a non-empty, non-whitespace title
3. **Valid Completion State**: completed MUST be a boolean value

---

## State Management

### Task Collection

- **Storage**: In-memory ordered collection (maintains insertion order)
- **Ordering**: Tasks MUST be stored and retrieved in creation order (FR-006, FR-014)
- **Lifetime**: Collection exists only during program runtime
- **Persistence**: None - all data lost on program exit

### ID Counter

- **Initial Value**: 0 (first task gets ID 1)
- **Increment**: +1 for each new task created
- **Reset**: Never reset during session (even if all tasks deleted)
- **Lifetime**: Exists only during program runtime

---

## Operations on Task

### Create Task

- **Inputs**: title (required), description (optional)
- **Outputs**: Created task with assigned ID
- **Side Effects**: Increments ID counter, adds task to collection
- **Validation**: Title MUST be non-empty after whitespace trimming

### Read Task (by ID)

- **Inputs**: Task ID
- **Outputs**: Task if found, error indicator if not found
- **Side Effects**: None

### Read All Tasks

- **Inputs**: None
- **Outputs**: Ordered list of all tasks (may be empty)
- **Side Effects**: None

### Update Task

- **Inputs**: Task ID, new title (optional), new description (optional)
- **Outputs**: Updated task if found, error indicator if not found
- **Side Effects**: Modifies task in collection
- **Validation**: If title provided, MUST be non-empty after whitespace trimming
- **Constraints**: ID and creation order MUST NOT change

### Delete Task

- **Inputs**: Task ID
- **Outputs**: Success indicator if found, error indicator if not found
- **Side Effects**: Removes task from collection
- **Note**: Deleted ID is NOT reused

### Mark Complete

- **Inputs**: Task ID
- **Outputs**: Updated task if found, error indicator if not found
- **Side Effects**: Sets completed = True

### Mark Incomplete

- **Inputs**: Task ID
- **Outputs**: Updated task if found, error indicator if not found
- **Side Effects**: Sets completed = False

---

## Error States

| Error Condition        | Applicable Operations              |
|------------------------|------------------------------------|
| Task not found         | Read, Update, Delete, Mark         |
| Empty title            | Create, Update                     |
| Whitespace-only title  | Create, Update                     |
| Invalid ID format      | Read, Update, Delete, Mark         |

---

## Data Model Diagram

```
┌─────────────────────────────────────┐
│              Task                   │
├─────────────────────────────────────┤
│ + id: Integer [PK, auto, immutable] │
│ + title: String [required]          │
│ + description: String [optional]    │
│ + completed: Boolean [default=false]│
├─────────────────────────────────────┤
│ Invariants:                         │
│ - id > 0                            │
│ - title.strip() != ""               │
│ - completed in {True, False}        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│          TaskCollection             │
├─────────────────────────────────────┤
│ - tasks: List<Task> [ordered]       │
│ - next_id: Integer [starts at 1]    │
├─────────────────────────────────────┤
│ + add(title, desc?) → Task          │
│ + get(id) → Task | None             │
│ + get_all() → List<Task>            │
│ + update(id, title?, desc?) → bool  │
│ + delete(id) → bool                 │
│ + mark_complete(id) → bool          │
│ + mark_incomplete(id) → bool        │
└─────────────────────────────────────┘
```

---

## Mapping to Functional Requirements

| Requirement | Data Model Element              |
|-------------|---------------------------------|
| FR-001      | Task.id (auto-generated)        |
| FR-002      | Task.title (required)           |
| FR-003      | Task.description (optional)     |
| FR-004      | Task.completed (default false)  |
| FR-005      | Task.id (immutable)             |
| FR-006      | TaskCollection ordering         |

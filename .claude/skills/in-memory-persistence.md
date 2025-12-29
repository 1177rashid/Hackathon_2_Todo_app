# In-Memory Persistence

## Purpose

This skill defines the data management layer for the Phase I Todo application. It handles all CRUD operations for tasks stored exclusively in memory, maintaining state throughout the session lifetime without any external persistence.

The skill is designed to:
- Manage task data in volatile memory structures
- Provide consistent CRUD operation interfaces
- Return structured responses for all operations
- Maintain data integrity during the session
- Support multiple consuming agents with a unified API

## State Management Strategy

### Data Structure

Tasks are stored in a single in-memory collection:

```
TaskStore = {
  tasks: Map<TaskId, Task> or List<Task>,
  nextId: Integer (for auto-increment)
}
```

### Task Entity Schema

```
Task = {
  id: Integer,           // Unique, immutable, auto-generated
  title: String,         // Required, 1-200 chars
  description: String?,  // Optional, max 1000 chars
  status: String         // "pending" | "completed"
}
```

### State Lifecycle

```
Application Start
       │
       ▼
┌─────────────────┐
│  Empty State    │  tasks: [], nextId: 1
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Active State   │  Operations modify state
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Session End    │  State is discarded
└─────────────────┘
```

### State Characteristics

| Property | Value |
|----------|-------|
| Persistence | None (volatile) |
| Scope | Single session |
| Initialization | Empty on start |
| Termination | Lost on exit |
| Thread Safety | Single-threaded (Phase I) |

## Supported Operations

### 1. add_task

Creates a new task and adds it to the store.

**Signature**:
```
add_task(title: String, description: String?) → OperationResult
```

**Input**:
| Parameter | Type | Required | Constraints |
|-----------|------|----------|-------------|
| title | String | Yes | 1-200 characters |
| description | String | No | Max 1000 characters |

**Behavior**:
1. Generate unique ID (nextId++)
2. Create task with status "pending"
3. Add task to store
4. Return success with new task

**Output**:
```
Success:
{
  success: true,
  operation: "add_task",
  task: {
    id: 1,
    title: "Buy groceries",
    description: "Milk, eggs, bread",
    status: "pending"
  }
}

Failure:
{
  success: false,
  operation: "add_task",
  error: {
    code: "VALIDATION_ERROR",
    message: "Title is required",
    field: "title"
  }
}
```

---

### 2. update_task

Modifies an existing task's title and/or description.

**Signature**:
```
update_task(task_id: Integer, title?: String, description?: String) → OperationResult
```

**Input**:
| Parameter | Type | Required | Constraints |
|-----------|------|----------|-------------|
| task_id | Integer | Yes | Must exist in store |
| title | String | No | 1-200 characters if provided |
| description | String | No | Max 1000 characters if provided |

**Behavior**:
1. Find task by ID
2. Validate task exists
3. Update only provided fields
4. Preserve unchanged fields
5. Return success with updated task

**Output**:
```
Success:
{
  success: true,
  operation: "update_task",
  task: {
    id: 1,
    title: "Buy groceries today",
    description: "Milk, eggs, bread",
    status: "pending"
  },
  changes: {
    title: { from: "Buy groceries", to: "Buy groceries today" }
  }
}

Failure:
{
  success: false,
  operation: "update_task",
  error: {
    code: "ID_NOT_FOUND",
    message: "No task found with ID 99",
    task_id: 99
  }
}
```

---

### 3. delete_task

Removes a task from the store permanently.

**Signature**:
```
delete_task(task_id: Integer) → OperationResult
```

**Input**:
| Parameter | Type | Required | Constraints |
|-----------|------|----------|-------------|
| task_id | Integer | Yes | Must exist in store |

**Behavior**:
1. Find task by ID
2. Validate task exists
3. Remove task from store
4. Return success with deleted task info

**Output**:
```
Success:
{
  success: true,
  operation: "delete_task",
  deleted: {
    id: 2,
    title: "Old task",
    description: null,
    status: "completed"
  }
}

Failure:
{
  success: false,
  operation: "delete_task",
  error: {
    code: "ID_NOT_FOUND",
    message: "No task found with ID 99",
    task_id: 99
  }
}
```

---

### 4. mark_complete

Changes a task's status from "pending" to "completed".

**Signature**:
```
mark_complete(task_id: Integer) → OperationResult
```

**Input**:
| Parameter | Type | Required | Constraints |
|-----------|------|----------|-------------|
| task_id | Integer | Yes | Must exist in store |

**Behavior**:
1. Find task by ID
2. Validate task exists
3. Update status to "completed"
4. Return success with updated task

**Output**:
```
Success:
{
  success: true,
  operation: "mark_complete",
  task: {
    id: 3,
    title: "Review PR",
    description: "Check the new feature branch",
    status: "completed"
  },
  previous_status: "pending"
}

Failure (not found):
{
  success: false,
  operation: "mark_complete",
  error: {
    code: "ID_NOT_FOUND",
    message: "No task found with ID 99",
    task_id: 99
  }
}

Info (already complete):
{
  success: true,
  operation: "mark_complete",
  task: { ... },
  note: "Task was already completed"
}
```

---

### 5. list_tasks

Retrieves all tasks or filters by status.

**Signature**:
```
list_tasks(filter_status?: String) → OperationResult
```

**Input**:
| Parameter | Type | Required | Constraints |
|-----------|------|----------|-------------|
| filter_status | String | No | "pending", "completed", or null (all) |

**Behavior**:
1. Retrieve all tasks from store
2. Apply filter if provided
3. Sort by ID (ascending)
4. Return task list with summary

**Output**:
```
Success (all tasks):
{
  success: true,
  operation: "list_tasks",
  filter: null,
  tasks: [
    { id: 1, title: "Task 1", description: null, status: "pending" },
    { id: 2, title: "Task 2", description: "Details", status: "completed" },
    { id: 3, title: "Task 3", description: null, status: "pending" }
  ],
  summary: {
    total: 3,
    pending: 2,
    completed: 1
  }
}

Success (filtered):
{
  success: true,
  operation: "list_tasks",
  filter: "pending",
  tasks: [
    { id: 1, title: "Task 1", description: null, status: "pending" },
    { id: 3, title: "Task 3", description: null, status: "pending" }
  ],
  summary: {
    total: 3,
    pending: 2,
    completed: 1,
    showing: 2
  }
}

Success (empty):
{
  success: true,
  operation: "list_tasks",
  filter: null,
  tasks: [],
  summary: {
    total: 0,
    pending: 0,
    completed: 0
  }
}
```

## Input/Output Structure

### Standard Input Format

All operations receive structured input:
```
{
  operation: String,      // Operation name
  params: {               // Operation-specific parameters
    [key]: value
  }
}
```

### Standard Output Format

All operations return structured results:

**Success Response**:
```
{
  success: true,
  operation: String,      // Operation that was performed
  [operation-specific fields]
}
```

**Failure Response**:
```
{
  success: false,
  operation: String,      // Operation that failed
  error: {
    code: String,         // Machine-readable error code
    message: String,      // Human-readable message
    [context fields]      // Additional error context
  }
}
```

### Error Codes

| Code | Description | Operations |
|------|-------------|------------|
| `VALIDATION_ERROR` | Input validation failed | add, update |
| `ID_NOT_FOUND` | Task ID doesn't exist | update, delete, complete |
| `INVALID_FILTER` | Invalid filter value | list |
| `INVALID_ID` | ID format is invalid | all ID-based ops |

## Operation Flow

### Pre-Operation Validation

Before any operation executes:
```
1. Validate input parameters exist
2. Validate parameter types
3. Validate parameter constraints
4. For ID-based ops: validate ID exists
5. If any validation fails: return error, do not modify state
```

### Post-Operation Response

After successful operation:
```
1. State is updated atomically
2. Response includes affected task(s)
3. Response includes operation metadata
4. State remains consistent
```

## Integration with Agents

### With in-memory-state-manager

Primary manager of this skill:
- Implements all operation logic
- Maintains the TaskStore
- Ensures state consistency

### With cli-interface

Consumer of operation results:
- Calls operations based on user input
- Receives structured responses
- Formats responses for display

### With task-domain-enforcer

Validation integration:
- Validates task entities before storage
- Enforces domain rules
- Ensures data integrity

### With id-integrity-manager

ID management integration:
- Generates unique IDs
- Validates ID existence
- Prevents duplicate IDs

### With task-validation-rules

Field validation integration:
- Validates title constraints
- Validates description constraints
- Validates status values

## State Isolation

### Session Boundaries

```
Session A                    Session B
┌─────────────┐             ┌─────────────┐
│ TaskStore A │             │ TaskStore B │
│  - Task 1   │             │  - Task 1   │ (different data)
│  - Task 2   │             │  - Task 2   │
└─────────────┘             └─────────────┘
      │                           │
      ▼                           ▼
   (exit)                      (exit)
      │                           │
      ▼                           ▼
   [lost]                      [lost]
```

### No Cross-Session Persistence

- Each session starts empty
- No data survives restart
- No file I/O (Phase I constraint)
- No external storage

## Concurrency Model (Phase I)

Phase I operates single-threaded:
- No concurrent access
- No race conditions
- No locking required
- Sequential operation processing

Future phases may require:
- Thread-safe collections
- Operation locking
- Transaction support

## Operation Summary Table

| Operation | Input | Output | State Change |
|-----------|-------|--------|--------------|
| add_task | title, description? | new task | +1 task |
| update_task | id, title?, description? | updated task | modify task |
| delete_task | id | deleted task info | -1 task |
| mark_complete | id | updated task | modify status |
| list_tasks | filter? | task array | none (read-only) |

## Guiding Principle

> "State lives in memory, changes through operations, and responds with structure. Every operation is validated before execution, every response is consistent in format, and every session starts fresh. In-memory means in-memory—no persistence, no exceptions."

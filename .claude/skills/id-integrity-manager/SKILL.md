# ID Integrity Manager

## Purpose

This skill ensures the integrity of task identifiers throughout the application lifecycle. It enforces that every task in the in-memory state has a unique, immutable ID and validates all operations that interact with task IDs.

The skill is designed to:
- Guarantee uniqueness of all task IDs in the system
- Enforce immutability of IDs once assigned
- Validate ID presence and format on every state operation
- Prevent data corruption from ID-related errors
- Provide clear feedback when ID violations occur

## When to Apply

This skill MUST be applied during:

1. **Add Operations** - When creating a new task
2. **Update Operations** - When modifying an existing task
3. **Delete Operations** - When removing a task
4. **Mark Complete Operations** - When changing task completion status
5. **Lookup Operations** - When retrieving a task by ID
6. **Bulk Operations** - When processing multiple tasks

This skill is triggered by:
- The `in-memory-state-manager` agent during CRUD operations
- The `task-domain-enforcer` agent when validating domain invariants
- Any agent that reads or writes task state
- Manual invocation when ID integrity is in question

## ID Specification

### ID Format Requirements

Task IDs must conform to these rules:

| Property | Requirement |
|----------|-------------|
| Type | Integer or UUID string |
| Uniqueness | Globally unique within state |
| Mutability | Immutable after creation |
| Nullability | Never null or undefined |
| Format | Consistent across all tasks |

### ID Lifecycle

```
Creation:
  [New Task Request] → [Generate Unique ID] → [Assign to Task] → [Store in State]

Usage:
  [Operation Request] → [Validate ID Exists] → [Perform Operation]

Immutability:
  [ID Assigned] → [LOCKED] → [Cannot be changed until task deleted]
```

## Validation Rules

### Rule 1: Presence Validation

Every task MUST have an ID field:

```
Check: task.id is defined AND task.id is not null AND task.id is not empty
Fail: Reject with "MISSING_ID"
```

### Rule 2: Type Validation

ID must be of the correct type:

```
Check: typeof task.id matches expected type (int or string)
Fail: Reject with "INVALID_ID_TYPE"
```

### Rule 3: Format Validation

ID must match the expected format:

```
For Integer IDs:
  Check: task.id > 0 AND Number.isInteger(task.id)
  Fail: Reject with "INVALID_ID_FORMAT"

For UUID IDs:
  Check: task.id matches UUID pattern
  Fail: Reject with "INVALID_ID_FORMAT"
```

### Rule 4: Uniqueness Validation (Add Operations)

New IDs must not already exist:

```
Check: state.tasks.find(t => t.id === newTask.id) === undefined
Fail: Reject with "DUPLICATE_ID"
```

### Rule 5: Existence Validation (Update/Delete/Complete Operations)

Referenced IDs must exist in state:

```
Check: state.tasks.find(t => t.id === targetId) !== undefined
Fail: Reject with "ID_NOT_FOUND"
```

### Rule 6: Immutability Validation (Update Operations)

ID field cannot be modified:

```
Check: existingTask.id === updatedTask.id
Fail: Reject with "ID_MODIFICATION_ATTEMPTED"
```

## Operation-Specific Validation

### Add Task

```
Validations:
1. [PRESENCE]   ID must be provided or auto-generated
2. [TYPE]       ID must be correct type
3. [FORMAT]     ID must match format rules
4. [UNIQUENESS] ID must not exist in state

On Pass: Create task with ID
On Fail: Reject operation, return error code
```

### Update Task

```
Validations:
1. [PRESENCE]     Target ID must be provided
2. [TYPE]         Target ID must be correct type
3. [EXISTENCE]    Target ID must exist in state
4. [IMMUTABILITY] Update payload must not change ID

On Pass: Update task fields (except ID)
On Fail: Reject operation, return error code
```

### Delete Task

```
Validations:
1. [PRESENCE]   Target ID must be provided
2. [TYPE]       Target ID must be correct type
3. [EXISTENCE]  Target ID must exist in state

On Pass: Remove task from state
On Fail: Reject operation, return error code
```

### Mark Complete

```
Validations:
1. [PRESENCE]   Target ID must be provided
2. [TYPE]       Target ID must be correct type
3. [EXISTENCE]  Target ID must exist in state
4. [IMMUTABILITY] Operation must not change ID

On Pass: Update completion status
On Fail: Reject operation, return error code
```

## Rejection Behavior

When an ID violation is detected, the manager MUST:

### 1. Halt the Operation

Do NOT allow the state-modifying operation to proceed.

### 2. Return Error Code

Provide a machine-readable error code:

| Error Code | Description |
|------------|-------------|
| `MISSING_ID` | No ID provided for task |
| `INVALID_ID_TYPE` | ID is not the expected type |
| `INVALID_ID_FORMAT` | ID does not match format rules |
| `DUPLICATE_ID` | ID already exists in state |
| `ID_NOT_FOUND` | Referenced ID does not exist |
| `ID_MODIFICATION_ATTEMPTED` | Tried to change an existing ID |

### 3. Provide Concise Feedback

Each rejection includes a short, actionable message:

```
ID INTEGRITY VIOLATION

Operation: [Add | Update | Delete | Mark Complete]
Error Code: [error code]
Task ID: [provided ID or "none"]

Reason:
  [One sentence explanation]

Resolution:
  [One sentence fix suggestion]
```

### Rejection Message Templates

**MISSING_ID**:
```
ID INTEGRITY VIOLATION

Operation: Add
Error Code: MISSING_ID
Task ID: none

Reason: Task cannot be created without an ID.
Resolution: Provide a valid ID or use auto-generation.
```

**INVALID_ID_TYPE**:
```
ID INTEGRITY VIOLATION

Operation: [operation]
Error Code: INVALID_ID_TYPE
Task ID: [provided value]

Reason: ID must be [integer/UUID], received [actual type].
Resolution: Provide ID as [expected type].
```

**INVALID_ID_FORMAT**:
```
ID INTEGRITY VIOLATION

Operation: [operation]
Error Code: INVALID_ID_FORMAT
Task ID: [provided value]

Reason: ID format is invalid. Expected [format description].
Resolution: Use [correct format example].
```

**DUPLICATE_ID**:
```
ID INTEGRITY VIOLATION

Operation: Add
Error Code: DUPLICATE_ID
Task ID: [provided ID]

Reason: A task with this ID already exists.
Resolution: Use a unique ID or rely on auto-generation.
```

**ID_NOT_FOUND**:
```
ID INTEGRITY VIOLATION

Operation: [Update | Delete | Mark Complete]
Error Code: ID_NOT_FOUND
Task ID: [provided ID]

Reason: No task exists with this ID.
Resolution: Verify the ID and retry with a valid task ID.
```

**ID_MODIFICATION_ATTEMPTED**:
```
ID INTEGRITY VIOLATION

Operation: Update
Error Code: ID_MODIFICATION_ATTEMPTED
Task ID: [original ID] → [attempted new ID]

Reason: Task IDs are immutable and cannot be changed.
Resolution: Remove ID field from update payload.
```

## Integration with Agents

### With in-memory-state-manager

Primary integration point:
- Validate all CRUD operations
- Enforce uniqueness in task collection
- Prevent invalid state transitions

### With task-domain-enforcer

Domain invariant enforcement:
- ID is a core domain property
- Immutability is a domain rule
- Validation occurs at domain boundary

### With cli-interface

User-facing validation:
- Translate error codes to user messages
- Prompt for valid ID input
- Display available task IDs on error

### With spec-driven-architect

Architectural validation:
- Ensure ID strategy matches spec
- Validate ID format against spec definition
- Confirm immutability requirement is enforced

## ID Generation Strategy

When auto-generating IDs, the manager recommends:

### Integer IDs (Simple)
```
Strategy: Sequential increment
Implementation: max(existing_ids) + 1 or counter
Pros: Simple, human-readable
Cons: Gaps on deletion, not globally unique
```

### UUID IDs (Robust)
```
Strategy: UUID v4 generation
Implementation: Standard UUID library
Pros: Globally unique, no coordination needed
Cons: Less human-readable
```

The specific strategy should be defined in the feature spec.

## Validation Checklist

Before any state operation, verify:

- [ ] ID is present (not null, not undefined, not empty)
- [ ] ID is correct type (matches spec definition)
- [ ] ID format is valid (matches pattern/rules)
- [ ] ID is unique (for Add operations)
- [ ] ID exists (for Update/Delete/Complete operations)
- [ ] ID is unchanged (for Update operations)

## State Consistency Guarantee

This skill guarantees:

1. **No Orphan Tasks**: Every task has exactly one valid ID
2. **No Duplicate IDs**: Each ID maps to exactly one task
3. **No ID Mutations**: Once set, IDs never change
4. **No Invalid References**: Operations only target existing IDs
5. **Fail-Safe Operations**: Invalid operations are rejected before state changes

## Guiding Principle

> "The ID is the task's identity. It is assigned once, verified always, and changed never. Every operation must prove the ID is valid before touching state. When validation fails, the operation fails—state remains untouched."

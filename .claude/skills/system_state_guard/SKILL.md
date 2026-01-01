# System State Guard

## Purpose

This skill protects the integrity of the in-memory application state across all operations. It enforces valid state transitions, prevents corruption, ensures data consistency, and guards against invalid updates that would compromise the application's logical correctness.

The skill is designed to:
- Enforce valid state transitions for all operations
- Prevent duplicate or corrupted task IDs
- Ensure completed tasks are immutable where required
- Guard against partial or invalid updates
- Maintain consistency across concurrent operations (single-threaded but conceptually)
- Protect invariants and constraints of the data model

## When This Skill Must Be Applied

This skill MUST be invoked:

1. **Before any state mutation** - Validate that operation can proceed safely
2. **During task creation** - Ensure new task doesn't corrupt state
3. **When updating tasks** - Verify update is valid and complete
4. **On task deletion** - Ensure no dangling references remain
5. **When marking tasks complete/incomplete** - Validate state transition
6. **Before returning state to user** - Ensure state is consistent

This skill is triggered by:
- `in-memory-state-manager` agent before any CRUD operation
- `task-validator` agent when validating task operations
- `error-handler-agent` when assessing operation feasibility
- Manual invocation during state debugging or auditing

## Core Responsibilities

### 1. Task ID Integrity

The guard enforces strict rules around task identification:

**ID Generation Rules:**
- Task IDs MUST be unique within the session
- IDs MUST be positive integers starting from 1
- IDs MUST be sequential without gaps (or use auto-increment mechanism)
- IDs MUST be immutable after task creation

**ID Validation:**
```
1. Check if ID already exists in task list
2. Verify ID is within valid range [1, current_max + 1]
3. Confirm ID is not reserved (e.g., 0, negative numbers)
4. Ensure ID format matches expected type (int)
```

**Duplicate Prevention:**
```
Scenario: Attempt to create task with existing ID

Guard Check:
  - Is ID already in use?
    YES → REJECT with specific error
    NO → Proceed with creation

State Invariant:
  ∀ id1, id2 in task_list: id1 == id2 ⇔ same task instance
```

### 2. State Transition Validity

The guard validates all state changes:

**Task Creation Transitions:**
```
Initial State: task does not exist
  → Operation: CREATE task with id=N
  → Valid Transitions:
      - N not in task list (unique ID)
      - Required fields present (title)
      - Optional fields have valid values or defaults
  → Final State: task exists in task_list[N-1] (0-indexed)
```

**Task Update Transitions:**
```
Initial State: task exists with state S
  → Operation: UPDATE task with changes C
  → Valid Transitions:
      - Task id exists in task list
      - Changes C are subset of allowed fields
      - New values meet field constraints
      - Immutable fields not modified
  → Final State: task exists with state S' where S' = S ∪ C
```

**Completion State Transitions:**
```
Initial State: task.status = pending|in-progress
  → Operation: MARK_COMPLETE
  → Valid Transitions:
      - Task is not already completed
      - Task is not cancelled
      - Task has not been deleted
  → Final State: task.status = completed

Inverse Transition (Mark Incomplete):
  → Operation: MARK_INCOMPLETE
  → Valid Transitions:
      - Task status is completed
      - Task is not deleted
  → Final State: task.status = pending
```

**Deletion Transitions:**
```
Initial State: task exists in task_list
  → Operation: DELETE task
  → Valid Transitions:
      - Task id exists
      - No references to this task remain (e.g., no recurrence dependencies)
      - Task list is not empty after deletion (unless deleting last task)
  → Final State: task removed from task_list, references cleaned
```

### 3. Immutable Field Protection

The guard enforces immutability on critical fields:

**Immutable Fields:**
- `id`: Task identifier - never changes after creation
- `created_at`: Task creation timestamp - never changes

**Immutable Update Attempts:**
```
Scenario: User attempts to change task ID

Guard Check:
  - Does update modify 'id' field?
    YES → REJECT with clear error
    NO → Proceed with update

Error Message:
  "Task ID is immutable and cannot be changed after creation."
```

**Mutable Fields (with restrictions):**
- `status`: Can change, but must follow valid state transitions
- `due_date`: Can change, but must remain valid datetime
- `recurrence_pattern`: Can change, but recurrence_policy_engine must validate
- `priority`, `tags`: Fully mutable

### 4. Partial Update Prevention

The guard prevents incomplete or partial state mutations:

**Update Completeness Check:**
```
Scenario: Update task with only some fields

Guard Validation:
  - Are all provided fields valid?
    NO → REJECT partially invalid update
    YES → Apply valid fields, reject invalid fields

Allowed Patterns:
  ✅ Update only priority (valid)
  ✅ Update only status (valid if transition allowed)
  ✅ Update both priority and tags (valid)
  ❌ Update priority with invalid value (reject entire operation or apply defaults)
```

**Transaction-Like Semantics:**
```
Guard Enforces: Either all changes apply, or none apply.

Example:
  Input: Update task #1 with priority="urgent", status="completed"
  Validation:
    - priority="urgent" → INVALID (not in allowed enum)
    - status="completed" → VALID (transition allowed)

  Guard Response: REJECT ENTIRE OPERATION
  Reason: Partial invalid state is worse than no state change
  Correction: Fix priority value to "high", then retry
```

### 5. State Consistency Enforcement

The guard maintains invariants across the entire task list:

**Global Invariants:**
```
Invariant 1: ID Uniqueness
  ∀ id1, id2 in tasks: id1 ≠ id2

Invariant 2: Sequential IDs (if using auto-increment)
  sorted(ids) == [1, 2, 3, ..., len(tasks)]

Invariant 3: No Dangling References
  For every recurring task X:
    If X.references_parent_id → task_list[parent_id] exists

Invariant 4: Status Enum Constraints
  ∀ task in tasks: task.status ∈ {pending, in-progress, completed, cancelled}
```

**Consistency Checks After Every Operation:**
1. Verify all IDs are unique
2. Confirm ID sequences are valid
3. Check for orphaned references
4. Validate all enum values are allowed
5. Ensure no task has conflicting properties

**Failure Response:**
```
STATE INCONSISTENCY DETECTED

Operation: [last operation performed]
Invariant Violated: [specific invariant name]
Details: [what is wrong]

Guard Action:
  - ROLLBACK to previous state (if possible)
  - Halt all further operations
  - Require state correction before proceeding
```

## Inputs & Outputs

### Inputs

| Input | Description | Example |
|--------|-------------|---------|
| `operation` | Type of state mutation | `"CREATE"`, `"UPDATE"`, `"DELETE"`, `"COMPLETE"`, `"INCOMPLETE"` |
| `task_id` | Task identifier (when applicable) | `1`, `42`, `null` (for CREATE) |
| `task_data` | Task properties for creation/update | `{title: "Buy milk", priority: "high"}` |
| `current_state` | Complete task list before operation | `[{id: 1, ...}, {id: 2, ...}]` |
| `constraints` | Validation rules from spec/constitution | `{"max_length": 500, "required_fields": ["title"]}` |

### Outputs

All outputs follow this structure:

```python
{
    "validation_result": "APPROVED" | "REJECTED" | "ROLLBACK_REQUIRED",
    "operation": str,
    "reason": str | None,
    "error_code": str | None,
    "suggestion": str | None,
    "invariant_status": "MAINTAINED" | "VIOLATED",
    "rollback_state": list | None  # Valid previous state if rollback possible
}
```

## Decision Rules

### Rule 1: Creation Validation

**Condition**: `operation == "CREATE"`
**Validation**:
- Task ID is unique
- Required fields present and non-empty
- Optional fields have valid values or default to None
- No invariant violations after creation

**Decision**: APPROVED if all validations pass

**Failure**: REJECT with specific field errors

### Rule 2: Update Validation

**Condition**: `operation == "UPDATE"`
**Validation**:
- Task ID exists in current state
- Mutable fields only (no ID modification)
- New values meet field constraints
- State transition is valid (e.g., status changes)
- No partial invalid updates (all-or-nothing)

**Decision**: APPROVED if task exists and updates are valid

**Failure**: REJECT with field-by-field error details

### Rule 3: Deletion Validation

**Condition**: `operation == "DELETE"`
**Validation**:
- Task ID exists in current state
- No references to this task remain (e.g., child tasks, recurrence links)
- Deletion won't create ID gaps that break invariants

**Decision**: APPROVED if task exists and no dependencies remain

**Failure**: REJECT with dependency information

### Rule 4: Completion Validation

**Condition**: `operation in ["COMPLETE", "INCOMPLETE"]`
**Validation**:
- Task ID exists
- Current status allows transition (not already in target state)
- If COMPLETE: task not cancelled
- If COMPLETE and recurring: recurrence_policy_engine approves regeneration
- If INCOMPLETE: task currently completed

**Decision**: APPROVED if transition is valid

**Failure**: REJECT with current status explanation

### Rule 5: Recurrence Handling

**Condition**: Task has recurrence_pattern and operation is "COMPLETE"
**Validation**:
- Recurrence policy engine validates pattern
- Due date calculation is valid
- New task instance won't create duplicate ID

**Decision**: APPROVED if recurrence engine approves

**Failure**: REJECT with recurrence-specific errors

### Rule 6: Global Consistency Check

**Condition**: After any approved operation
**Validation**:
- ID uniqueness invariant maintained
- Sequential IDs maintained (if applicable)
- No dangling references exist
- All enum values are valid

**Decision**: State is VALID if all invariants pass

**Failure**: ROLLBACK_REQUIRED with invariant details

## Constraints

### Global Constraints

1. **No Corrupt State**: Guard rejects any operation that creates inconsistent state
2. **Atomic Operations**: Either all changes apply or none (transaction semantics)
3. **Immutable IDs**: Task IDs never change after creation
4. **Reference Integrity**: No dangling references after deletion
5. **Validation First**: Every mutation passes validation before execution

### Phase I Constraints

1. **In-Memory Only**: State exists in runtime structures only
2. **No Concurrency**: Single-threaded, single-user (conceptual consistency only)
3. **Simple Types**: State uses standard library types (dict, list, primitive values)
4. **No Transactions**: No database transaction semantics (manual validation only)
5. **No Recovery**: No persistence or recovery mechanisms (in-memory loss is possible)

## Failure Handling

### Failure Scenario 1: Duplicate Task ID

**Input**: `CREATE` task with id=3 when task 3 already exists

**Guard Response**:
```
STATE GUARD: REJECTED

Operation: CREATE
Task ID: 3

Reason: Task ID #3 already exists in task list.

State Invariant Violated: ID Uniqueness

Suggestion:
  - Check existing tasks with 'list' command
  - Use the next available ID (#4)
  - Or allow system to auto-generate ID

Current State:
  Tasks: 1 (Buy milk), 2 (Walk dog), 3 (Call mom)

Validation Result: REJECTED - Duplicate ID
```

### Failure Scenario 2: Updating Immutable Field

**Input**: `UPDATE` task #1 with id=99

**Guard Response**:
```
STATE GUARD: REJECTED

Operation: UPDATE
Task ID: 1
Update: id → 99

Reason: Task ID is immutable and cannot be changed after creation.

Constraint Violated: Immutable Field Protection

Suggestion:
  - Delete task #1 and create new task with ID #99
  - Or keep original ID #1 and update other fields

Allowed Mutable Fields:
  - title, description, status, priority, tags, due_date, recurrence_pattern

Validation Result: REJECTED - Attempt to modify immutable field
```

### Failure Scenario 3: Invalid State Transition

**Input**: `COMPLETE` task #5 where task.status == "cancelled"

**Guard Response**:
```
STATE GUARD: REJECTED

Operation: COMPLETE
Task ID: 5

Reason: Cannot mark cancelled task as complete.

Current State:
  Task #5 status: cancelled

Allowed Status Transitions:
  - pending → in-progress
  - pending → completed
  - in-progress → completed
  - completed → pending (undo)
  - any status → cancelled

Invalid Transition:
  - cancelled → completed (not allowed)

Suggestion:
  - First change task status from cancelled to pending
  - Then mark task as complete
  - Or delete the cancelled task and create a new one

Validation Result: REJECTED - Invalid state transition
```

### Failure Scenario 4: Deleting Task with Dependencies

**Input**: `DELETE` task #1 which is parent to recurring task #5

**Guard Response**:
```
STATE GUARD: REJECTED

Operation: DELETE
Task ID: 1

Reason: Task #1 has dependent tasks and cannot be deleted.

Dependencies Detected:
  - Task #5 (generated from recurrence of #1)
  - Task #8 (generated from recurrence of #1)

State Invariant: No Dangling References

Suggestion:
  - Option 1: Delete all dependent tasks (#5, #8) first
  - Option 2: Stop recurrence on #1 before deleting
  - Option 3: Keep #1 and mark it complete instead

Validation Result: REJECTED - Dependent tasks exist
```

### Failure Scenario 5: Partial Invalid Update

**Input**: `UPDATE` task #2 with priority="urgent" (invalid) and status="completed" (valid)

**Guard Response**:
```
STATE GUARD: REJECTED

Operation: UPDATE
Task ID: 2

Reason: Update contains invalid field(s). Operation rejected entirely.

Field-by-Field Validation:
  ❌ priority="urgent" → INVALID (allowed: low, medium, high)
  ✅ status="completed" → VALID

Guard Policy:
  All-or-nothing update semantics prevent partial state corruption.

Suggestion:
  - Correct priority value to "high" (closest valid option)
  - Retry update with both valid values
  - Or update status only in one operation, then correct priority

Validation Result: REJECTED - Partial invalid update
```

### Failure Scenario 6: Global Invariant Violation

**Input**: After operation, task list has duplicate IDs due to bug

**Guard Response**:
```
STATE GUARD: INCONSISTENCY DETECTED

Operation: [last operation performed]
Invariant Violated: ID Uniqueness

Details:
  Duplicate IDs found: #3, #7
  Task #3: "Buy groceries"
  Task #7: "Buy groceries" (duplicate ID)

Guard Action: ROLLBACK REQUIRED

Suggestion:
  - Previous state restored
  - Investigate bug in ID generation logic
  - Fix and retry operation

Rollback State Available: YES
  Restoring to state before operation...

Validation Result: ROLLBACK_REQUIRED - State inconsistency
```

## Reusability Notes

### Cross-Phase Application

This skill is designed for reuse across all project phases:

- **Phase I**: Enforces in-memory state consistency, simple validation
- **Phase II**: Will extend with database transaction semantics, ACID properties
- **Phase III**: Will add API state validation, concurrent access protection
- **Phase IV+**: Will adapt to distributed state, eventual consistency

The skill does NOT hardcode Phase I rules. Instead it:
1. Applies state invariants defined in data model
2. Validates against constraints from specification
3. Adapts to persistence mechanisms (in-memory, database, distributed)

### Extension Points

For future phases, guard can be extended with:
- Database transaction validation (isolation, durability)
- Concurrency control (optimistic/pessimistic locking)
- Distributed state validation (CAP theorem considerations)
- Event sourcing validation (event replay consistency)
- State machine enforcement for complex workflows

## Conceptual Example

**Scenario**: User updates task #3 with priority and status change

**Initial State**:
```
Task List:
  1: {id: 1, title: "Buy milk", status: "pending", priority: None}
  2: {id: 2, title: "Walk dog", status: "in-progress", priority: "medium"}
  3: {id: 3, title: "Write code", status: "pending", priority: None}
```

**Input Operation**:
```
UPDATE task #3:
  - priority: "high"
  - status: "completed"
```

**Guard Validation Process**:

1. **ID Existence Check**: ✅ Task #3 exists
2. **Immutable Field Check**: ✅ No attempt to modify id
3. **Field Validity Check**:
   - priority="high" → ✅ Valid (allowed enum value)
   - status="completed" → ✅ Valid (transition: pending→completed)
4. **State Transition Check**: ✅ pending→completed is allowed
5. **Partial Update Check**: ✅ All fields valid, no partial rejection
6. **Post-Operation Invariant Check**:
   - ID uniqueness → ✅ Maintained
   - No references broken → ✅ Maintained
   - Enum values → ✅ All valid

**Guard Response**:
```
STATE GUARD: APPROVED

Operation: UPDATE
Task ID: 3
Changes Applied: priority → "high", status → "completed"

Validation Summary:
  ✅ Task exists
  ✅ Mutable fields only
  ✅ Valid field values
  ✅ Valid state transition
  ✅ All invariants maintained

Final State:
  1: {id: 1, title: "Buy milk", status: "pending", priority: None}
  2: {id: 2, title: "Walk dog", status: "in-progress", priority: "medium"}
  3: {id: 3, title: "Write code", status: "completed", priority: "high"}

Validation Result: APPROVED - All checks passed
```

**Outcome**: Update applied successfully, state remains consistent.

## Integration with Other Agents/Skills

### With in-memory-state-manager

- Guard validates every state mutation before manager executes
- Manager reports state to guard for consistency checks
- Coordination: Guard protects, manager implements

### With task-validator

- Guard validates state integrity, validator validates business rules
- Both run before any operation proceeds
- Coordination: Guard ensures state is consistent, validator ensures task is valid

### With recurrence_policy_engine

- Guard validates completion operation, engine validates recurrence rules
- Both must approve for recurring task completion
- Coordination: Guard ensures state safety, engine ensures recurrence correctness

### With task-domain-enforcer

- Guard protects state structure, enforcer protects domain invariants
- Enforcer defines WHAT properties can exist, guard ensures HOW they change safely
- Coordination: Enforcer provides rules, guard enforces them

### With error-handler-agent

- Guard provides validation failures, handler formats user messages
- Handler receives error codes and suggestions from guard
- Coordination: Guard detects issues, handler communicates them to user

## Guiding Principle

> "State is the foundation of correctness. Every mutation must be validated, every transition must be safe, and every operation must maintain invariants. The guard is the shield that protects the application's logical integrity from corruption, inconsistency, and invalidity."

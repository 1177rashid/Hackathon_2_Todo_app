# Recurrence Policy Engine

## Purpose

This skill defines and enforces recurrence rules independently of implementation logic. It serves as the authoritative source of truth for how recurring tasks behave, what patterns are allowed, and how recurrence interacts with task lifecycle events.

The skill is designed to:
- Specify allowed recurrence patterns (daily, weekly, monthly)
- Validate recurrence inputs against defined patterns
- Define completion-to-regeneration policy
- Reject invalid or ambiguous recurrence definitions
- Maintain separation between recurrence rules and implementation

## When This Skill Must Be Applied

This skill MUST be invoked:

1. **When creating recurring tasks** - Validate recurrence pattern is allowed
2. **When modifying recurrence settings** - Ensure new pattern is valid
3. **Before marking recurring tasks complete** - Validate regeneration rules
4. **When stopping recurrence** - Confirm action is valid
5. **During recurrence edge case handling** - Apply defined policy
6. **Before implementation of recurrence logic** - Ensure code follows policy

This skill is triggered by:
- `task-domain-enforcer` agent when validating task creation
- `system_state_guard` agent when handling completion transitions
- `error-handler-agent` when assessing recurrence-related errors
- Manual invocation during architectural decisions about recurrence

## Core Responsibilities

### 1. Recurrence Pattern Specification

The engine defines what recurrence patterns are valid:

**Allowed Patterns (Phase I - Advanced Tier)**:

| Pattern | Description | Required Fields | Optional Fields |
|---------|-------------|------------------|-----------------|
| `daily` | Task repeats every day | `due_date` | None |
| `weekly` | Task repeats every week | `due_date` | None |
| `monthly` | Task repeats every month | `due_date` | None |
| `none` | Task does not recur | None | None |

**Pattern Definitions**:

**Daily**:
```
Frequency: Once per day
Due Date Increment: +1 day
Day Boundary: None (occurs at same time as original due date)
Example:
  - Original due: 2025-01-01 09:00
  - Next recurrence: 2025-01-02 09:00
```

**Weekly**:
```
Frequency: Once per week
Due Date Increment: +7 days
Week Boundary: None (occurs on same day of week as original)
Example:
  - Original due: 2025-01-01 (Wednesday)
  - Next recurrence: 2025-01-08 (Wednesday)
```

**Monthly**:
```
Frequency: Once per month
Due Date Increment: +1 month
Month Boundary: Adjust for shorter months (e.g., Jan 31 → Feb 28/29)
Edge Case Handling:
  - If due date is last day of month, use last day of next month
  - If original day doesn't exist in next month (e.g., Feb 30), use last valid day
Examples:
  - Original due: 2025-01-31 → Next: 2025-02-28 (or 2025-02-29 in leap year)
  - Original due: 2025-01-15 → Next: 2025-02-15
```

**None**:
```
Frequency: Never repeats
Behavior: Standard non-recurring task
Due Date Increment: N/A
```

### 2. Recurrence Input Validation

The engine validates all recurrence-related inputs:

**Creation Validation**:
```
Input: Create task with recurrence pattern

Validation Rules:
1. If recurrence_pattern is not None:
   a. Pattern must be in allowed set {daily, weekly, monthly}
   b. Task MUST have a due_date
   c. Due_date must be valid datetime
2. If recurrence_pattern is None:
   a. No validation required (standard task)
3. All recurrence fields must be complete:
   a. frequency (if specified) must be valid
   b. interval (if specified) must be positive integer
```

**Modification Validation**:
```
Input: Update task's recurrence settings

Validation Rules:
1. Old recurrence can be changed to new recurrence
2. New recurrence must follow creation validation rules
3. Stopping recurrence (set to None) is always allowed
4. If recurrence was active, previous instances remain valid
5. If recurrence becomes active, due_date must exist
```

**Edge Case Validations**:
```
Edge Case 1: Due Date in Past
  Input: Create recurring task with due_date yesterday
  Validation: ALLOWED (first instance can be overdue)
  Policy: Recurrence doesn't require future due dates

Edge Case 2: Monthly with Feb 30
  Input: Create monthly recurrence due on Feb 30
  Validation: REJECTED
  Policy: Invalid date combination, February doesn't have day 30

Edge Case 3: Monthly with Jan 31
  Input: Create monthly recurrence due on Jan 31
  Validation: ALLOWED with adjustment
  Policy: Next recurrence adjusts to Feb 28/29 (last valid day)

Edge Case 4: No Due Date with Recurrence
  Input: Create task with recurrence but no due_date
  Validation: REJECTED
  Policy: Recurring tasks require due dates for calculation
```

### 3. Completion-to-Regeneration Policy

The engine defines what happens when recurring tasks are marked complete:

**Regeneration Rules**:
```
Trigger: Task marked as complete AND task.recurring_pattern != None

Policy:
1. Original task becomes completed (status = completed)
2. New task instance is created with:
   - Same title, description, priority, tags
   - status = pending (or in-progress if spec requires)
   - due_date = calculated based on recurrence pattern
   - recurrence_pattern = same as original task
   - id = auto-generated new unique ID
3. Original task remains in task list (completed state)
4. New task is added to task list
5. User receives confirmation of regeneration
```

**Due Date Calculation Logic**:

**Daily**:
```python
next_due_date = original_due_date + timedelta(days=1)
# Same time of day, next day
```

**Weekly**:
```python
next_due_date = original_due_date + timedelta(weeks=1)
# Same day of week, next week
```

**Monthly**:
```python
# Add 1 month, then validate
next_due_date = original_due_date + relativedelta(months=1)

# Edge case: Adjust if original was last day of month
if original_due_date.day == last_day_of_month(original_due_date.month):
    next_due_date = last_day_of_month(next_due_date.month, next_due_date.year)

# Edge case: Adjust if original day doesn't exist in next month
if original_due_date.day > days_in_month(next_due_date.month):
    next_due_date = last_day_of_month(next_due_date.month, next_due_date.year)
```

**Regeneration Constraints**:
```
Constraint 1: No Duplicate Tasks
  - New task must have unique ID
  - New task must be distinguishable from original
  - System ensures no infinite loops

Constraint 2: Due Date Must Advance
  - Calculated next_due_date must be > original_due_date
  - If calculation fails (e.g., error), regeneration is blocked
  - User receives error with explanation

Constraint 3: Preserve Properties
  - All optional fields copied from original task
  - Exception: completion status (always reset)
  - Recurrence pattern preserved for continued recurrence

Constraint 4: Stop Condition
  - User can stop recurrence at any time
  - Stopped recurrence does not regenerate
  - Task with stopped recurrence can be completed normally
```

### 4. Recurrence Termination Rules

The engine defines how recurrence stops:

**Termination Methods**:

**Method 1: User Stops Recurrence**
```
Trigger: User explicitly stops recurrence on task

Policy:
1. recurrence_pattern set to None
2. No further regenerations occur
3. Task can be completed normally (does not regenerate)
4. Previous regenerated instances remain valid
```

**Method 2: Task Deletion**
```
Trigger: User deletes task with recurrence_pattern

Policy:
1. Task is removed from task list
2. All future regenerations are cancelled
3. Previously regenerated instances are NOT automatically deleted
4. User must delete instances individually if desired
```

**Method 3: Modification to Non-Recurring**
```
Trigger: User modifies recurrence_pattern to None

Policy:
1. Behaves same as "User Stops Recurrence"
2. Task becomes standard non-recurring task
3. Future completions do not trigger regeneration
```

### 5. Recurrence Visibility and Identification

The engine defines how recurring tasks are distinguished:

**Visual Indicators**:
```
Display Indicators:
- Icon: 🔄 (or equivalent CLI marker)
- Label: "Recurring" or pattern name
- Color: Distinct from non-recurring tasks (if CLI supports)

Example Display:
  🔄 [1] Buy groceries (recurring: daily)
  [2] Walk dog
  🔄 [3] Pay bills (recurring: monthly)
```

**Identification Rules**:
```
Rule 1: All Recurring Tasks Marked
  - Any task with recurrence_pattern != None is marked
  - Indicator appears in task list view

Rule 2: Recurrence Pattern Displayed
  - Pattern name shown when possible (daily, weekly, monthly)
  - Next due date calculated and displayed (optional)

Rule 3: Recurrence Status Visible
  - User can see if task is currently recurring
  - User can see if recurrence has been stopped
  - Stopped tasks show as "(recurrence stopped)" or similar
```

## Inputs & Outputs

### Inputs

| Input | Description | Example |
|--------|-------------|---------|
| `recurrence_pattern` | Recurrence pattern for task | `"daily"`, `"weekly"`, `"monthly"`, `None` |
| `due_date` | Task's due date | `datetime(2025, 1, 15, 9, 0)` |
| `task_properties` | All task properties to copy | `{title: "...", description: "...", priority: "high"}` |
| `operation` | Type of recurrence operation | `"CREATE"`, `"UPDATE"`, `"COMPLETE"`, `"STOP"` |

### Outputs

All outputs follow this structure:

```python
{
    "validation_result": "APPROVED" | "REJECTED",
    "regeneration_decision": "REGENERATE" | "NO_REGENERATE" | None,
    "next_due_date": datetime | None,
    "error_code": str | None,
    "error_message": str | None,
    "warnings": list[str],
    "suggestion": str | None
}
```

## Decision Rules

### Rule 1: Recurrence Creation

**Condition**: `operation == "CREATE"` with recurrence pattern
**Validation**:
- Pattern is in allowed set
- Due date is provided
- Due date is valid datetime
- Date combination is valid (e.g., not Feb 30)

**Decision**: APPROVED if all validations pass

**Failure**: REJECTED with specific error

### Rule 2: Recurrence Modification

**Condition**: `operation == "UPDATE"` changing recurrence pattern
**Validation**:
- New pattern follows creation validation
- If stopping (None), always allowed
- If starting, all creation rules apply

**Decision**: APPROVED if new pattern is valid

**Failure**: REJECTED with specific error

### Rule 3: Completion Regeneration

**Condition**: `operation == "COMPLETE"` on recurring task
**Validation**:
- Task has recurrence_pattern != None
- Task has due_date
- Next due date can be calculated
- New task ID is unique

**Decision**: REGENERATE if validations pass

**Failure**: NO_REGENERATE if validation fails

### Rule 4: Recurrence Stopping

**Condition**: `operation in ["STOP", "DELETE", "UPDATE"]` stopping recurrence
**Validation**:
- No validation required for stopping
- Recurrence is simply disabled

**Decision**: Always APPROVED

**Note**: Deletion has additional state management (handled by system_state_guard)

## Constraints

### Global Constraints

1. **Due Date Required**: All recurring tasks must have due_date
2. **Pattern Validation**: Only defined patterns are allowed
3. **No Infinite Loops**: Regeneration must advance due dates, not repeat same date
4. **Property Preservation**: All task properties except completion status are copied
5. **User Control**: Users can stop recurrence at any time

### Phase I Constraints

1. **Simple Patterns**: Only daily, weekly, monthly supported (no complex cron-like expressions)
2. **Single Instance per Completion**: One regeneration per completion event
3. **No Batch Regeneration**: No multiple future instances created at once
4. **Manual Stop Only**: No automatic termination based on count or date
5. **In-Memory Only**: Recurrence state exists only in runtime

## Failure Handling

### Failure Scenario 1: Recurrence Without Due Date

**Input**: `CREATE` task with recurrence_pattern="daily" but no due_date

**Engine Response**:
```
RECURRENCE POLICY ENGINE: REJECTED

Operation: CREATE recurring task
Pattern: daily

Reason: Recurring tasks require a due date for calculation
           of next occurrence dates.

Error Code: R001
Error Message: Cannot create recurring task without due date.

Policy Violation:
  Recurrence Pattern Definition (Policy Section 1)
  Rule: All recurring tasks must have a due_date

Suggestion:
  - Provide a due date when creating the task
  - Example: "add Buy groceries --due 2025-01-15 --recurrence daily"

Validation Result: REJECTED - Missing due date
```

### Failure Scenario 2: Invalid Recurrence Pattern

**Input**: `CREATE` task with recurrence_pattern="hourly"

**Engine Response**:
```
RECURRENCE POLICY ENGINE: REJECTED

Operation: CREATE recurring task
Pattern: hourly

Reason: 'hourly' is not a valid recurrence pattern.
           Allowed patterns: daily, weekly, monthly, none.

Error Code: R002
Error Message: Invalid recurrence pattern 'hourly'.

Policy Violation:
  Recurrence Pattern Specification (Policy Section 1)
  Rule: Only defined patterns are allowed

Suggestion:
  - Use one of the allowed patterns
  - Example: --recurrence daily, --recurrence weekly, --recurrence monthly
  - Or omit recurrence for non-recurring task

Allowed Patterns:
  - daily: Task repeats every day
  - weekly: Task repeats every week
  - monthly: Task repeats every month
  - none: Task does not recur

Validation Result: REJECTED - Invalid pattern
```

### Failure Scenario 3: Invalid Date Combination

**Input**: `CREATE` task with recurrence_pattern="monthly" and due_date="2025-02-30"

**Engine Response**:
```
RECURRENCE POLICY ENGINE: REJECTED

Operation: CREATE recurring task
Pattern: monthly
Due Date: 2025-02-30

Reason: Invalid date combination for monthly recurrence.
           February 2025 does not have day 30.

Error Code: R003
Error Message: Invalid due date for monthly recurrence.

Policy Violation:
  Recurrence Pattern Specification (Policy Section 1)
  Rule: Monthly recurrence requires valid date in target month

Suggestion:
  - Use a valid date for February
  - Examples: 2025-02-28 (non-leap year) or 2025-02-29 (leap year)
  - Or choose a different month for your due date

Date Adjustment Policy:
  - If original due date is last day of month (e.g., Jan 31),
    next recurrence adjusts to last day of next month (e.g., Feb 28/29)
  - If original day doesn't exist in next month,
    recurrence uses last valid day

Validation Result: REJECTED - Invalid date
```

### Failure Scenario 4: Regeneration Calculation Failure

**Input**: `COMPLETE` recurring task where next_due_date calculation fails

**Engine Response**:
```
RECURRENCE POLICY ENGINE: NO_REGENERATE

Operation: COMPLETE recurring task
Task ID: 5
Pattern: monthly
Current Due: 2025-01-31

Reason: Cannot calculate next due date for regeneration.

Error Code: R004
Error Message: Failed to calculate next occurrence date.

Policy Impact:
  Task will be marked complete but not regenerated.
  User can create a new task manually if needed.

Debugging Information:
  - Current due date: 2025-01-31
  - Recurrence pattern: monthly
  - Calculation error: [specific error details]

Suggestion:
  - Manually create the next task instance
  - Check if due date is valid (e.g., not Feb 30)
  - Report this issue for investigation

Validation Result: NO_REGENERATE - Calculation failure
```

### Failure Scenario 5: Stopping Recurrence with Regenerated Tasks

**Input**: `STOP` recurrence on task that has already regenerated instances

**Engine Response**:
```
RECURRENCE POLICY ENGINE: APPROVED

Operation: STOP recurrence
Task ID: 3

Validation Result: APPROVED

Policy Applied:
  - Recurrence stopped for task #3
  - Previously regenerated instances (e.g., #7, #12) remain valid
  - No future regenerations will occur

User Guidance:
  Task #3 is no longer recurring.
  Generated instances (#7, #12) can be managed separately.

  To remove regenerated tasks:
  - Delete them individually: delete #7, delete #12

No Violations Detected
Validation Result: APPROVED - Recurrence stopped
```

## Reusability Notes

### Cross-Phase Application

This skill is designed for reuse across all project phases:

- **Phase I**: Simple patterns (daily, weekly, monthly), no persistence
- **Phase II**: Will add recurrence history tracking, skip capability
- **Phase III**: Will add API-defined patterns, user customization
- **Phase IV+**: Will adapt to distributed recurrence, team recurrence

The skill does NOT hardcode Phase I rules. Instead it:
1. Defines recurrence patterns as configuration
2. Separates policy from implementation
3. Adapts pattern definitions over time

### Extension Points

For future phases, engine can be extended with:
- Custom recurrence intervals (e.g., every 2 weeks, every 3 months)
- End conditions (recurrence stops after N occurrences, until specific date)
- Skip capability (skip specific recurrences temporarily)
- Business-day-aware recurrence (weekdays only, exclude holidays)
- Complex patterns (cron-like expressions)
- Team recurrence (shared recurring tasks across users)

## Conceptual Example

**Scenario**: User completes daily recurring task due 2025-01-15

**Initial Task**:
```
Task #15
  title: "Take medication"
  recurrence_pattern: "daily"
  due_date: 2025-01-15 09:00
  status: "pending"
  priority: "high"
  tags: ["health"]
```

**Input Operation**:
```
COMPLETE task #15
```

**Engine Validation Process**:

1. **Recurrence Check**:
   ```
   Does task have recurrence_pattern?
   YES: "daily"
   ```

2. **Due Date Calculation**:
   ```
   next_due_date = 2025-01-15 09:00 + 1 day
   next_due_date = 2025-01-16 09:00
   ```

3. **Property Preservation**:
   ```
   Copy from original task:
   - title: "Take medication"
   - description: [if exists]
   - priority: "high"
   - tags: ["health"]
   - recurrence_pattern: "daily"

   Reset:
   - status: "pending" (for new instance)
   - id: new auto-generated (e.g., #16)
   ```

4. **Validation**:
   ```
   - Due date calculation succeeded? YES
   - New task ID unique? YES (#16 not in use)
   - Pattern valid? YES (still "daily")
   ```

**Engine Response**:
```
RECURRENCE POLICY ENGINE: APPROVED - REGENERATE

Operation: COMPLETE recurring task
Task ID: 15
Pattern: daily

Regeneration Decision: REGENERATE

New Task Instance Created:
  ID: #16
  title: "Take medication"
  recurrence_pattern: "daily"
  due_date: 2025-01-16 09:00
  status: "pending"
  priority: "high"
  tags: ["health"]

Original Task Status:
  Task #15 marked as completed

Validation Result: APPROVED - Regeneration successful
```

**Outcome**:
- Original task #15 is marked completed
- New task #16 is created with all properties copied
- Due date advanced to next day (2025-01-16)
- Recurrence pattern preserved for continued regeneration

## Integration with Other Agents/Skills

### With task-domain-enforcer

- Engine validates recurrence patterns during task creation
- Domain enforcer applies recurrence rules to domain model
- Coordination: Engine defines rules, enforcer enforces invariants

### With system_state_guard

- Guard validates state transition, engine validates regeneration rules
- Both must approve for completion to proceed
- Coordination: Guard ensures state safety, engine ensures recurrence correctness

### With error-handler-agent

- Engine provides validation failures, handler formats user messages
- Handler receives error codes and suggestions from engine
- Coordination: Engine detects issues, handler communicates them to user

### With task-model-evolution-guard

- Guard validates recurrence field addition to model
- Engine defines what values recurrence field can hold
- Coordination: Guard ensures field exists safely, engine defines valid values

## Guiding Principle

> "Recurrence is a defined policy, not arbitrary behavior. The engine serves as source of truth for how recurring tasks behave. Implementation follows policy, not the reverse. This separation ensures predictable, documented, and evolvable recurrence behavior across all phases."

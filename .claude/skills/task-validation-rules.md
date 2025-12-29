# Task Validation Rules

## Purpose

This skill enforces domain validation rules for task entities in Phase I of the application. It ensures all task data conforms to defined constraints before being accepted into the system, maintaining data integrity and consistent behavior across all operations.

The skill is designed to:
- Validate task properties against defined constraints
- Enforce required fields and value limits
- Restrict status to allowed values only
- Provide clear, actionable feedback on validation failures
- Maintain consistency across all task-modifying operations

## Validation Rules

### Rule 1: Title (Required)

| Property | Constraint |
|----------|------------|
| Field | `title` |
| Required | Yes |
| Type | String |
| Min Length | 1 character |
| Max Length | 200 characters |
| Whitespace | Trimmed; cannot be only whitespace |

**Validation Logic**:
```
1. title must be present
2. title must be a string
3. title.trim().length >= 1
4. title.trim().length <= 200
```

**Error Codes**:
- `TITLE_REQUIRED` - Title is missing or null
- `TITLE_EMPTY` - Title is empty or only whitespace
- `TITLE_TOO_LONG` - Title exceeds 200 characters

### Rule 2: Description (Optional)

| Property | Constraint |
|----------|------------|
| Field | `description` |
| Required | No |
| Type | String or null |
| Min Length | 0 characters (when provided) |
| Max Length | 1000 characters |

**Validation Logic**:
```
1. If description is provided:
   a. description must be a string
   b. description.length <= 1000
2. If description is null/undefined: Valid (optional field)
```

**Error Codes**:
- `DESCRIPTION_TOO_LONG` - Description exceeds 1000 characters
- `DESCRIPTION_INVALID_TYPE` - Description is not a string

### Rule 3: Status (Restricted Values)

| Property | Constraint |
|----------|------------|
| Field | `status` |
| Required | Yes (with default) |
| Type | String |
| Allowed Values | `"pending"`, `"completed"` |
| Default | `"pending"` |
| Case Sensitive | Yes |

**Validation Logic**:
```
1. status must be present (or default applied)
2. status must be a string
3. status must be exactly "pending" or "completed"
4. No other values are permitted
```

**Error Codes**:
- `STATUS_REQUIRED` - Status is missing and no default applied
- `STATUS_INVALID` - Status is not "pending" or "completed"

## When to Apply

### Add Task Operation

Validate ALL fields:
```
Required Validations:
- [TITLE]       Must be present, 1-200 chars
- [DESCRIPTION] If provided, max 1000 chars
- [STATUS]      Must be "pending" or "completed" (default: "pending")

Timing: Before task is added to state
On Fail: Reject add operation entirely
```

### Update Task Operation

Validate ONLY fields being updated:
```
Conditional Validations:
- [TITLE]       If title in payload: validate 1-200 chars
- [DESCRIPTION] If description in payload: validate max 1000 chars
- [STATUS]      If status in payload: validate allowed values

Timing: Before update is applied to state
On Fail: Reject update operation entirely
```

### Mark Complete Operation

Validate status transition:
```
Required Validations:
- [STATUS] New status must be "completed"
- [STATUS] Transition from any status to "completed" is valid

Timing: Before status change is applied
On Fail: Reject mark complete operation
```

## How to Apply

### Step 1: Collect Input

Gather the task data to be validated:
```
input = {
  title: [user-provided or existing],
  description: [user-provided or existing or null],
  status: [user-provided or existing or default]
}
```

### Step 2: Run Validation Pipeline

Execute validations in order:
```
1. Validate title (if required for operation)
2. Validate description (if provided)
3. Validate status (if required for operation)
4. Collect all errors (do not stop at first error)
```

### Step 3: Evaluate Results

Determine pass/fail:
```
If errors.length === 0:
  → PASS: Proceed with operation
Else:
  → FAIL: Return all validation errors
```

### Step 4: Return Feedback

Provide clear response:
```
On Pass:
  { valid: true, data: validatedTask }

On Fail:
  { valid: false, errors: [array of error objects] }
```

## Feedback on Violations

### Error Response Structure

Each validation error includes:
```
{
  field: "[field name]",
  code: "[ERROR_CODE]",
  message: "[Human-readable message]",
  constraint: "[Constraint that was violated]",
  received: "[Actual value received]"
}
```

### Error Messages by Field

#### Title Errors

**TITLE_REQUIRED**:
```
VALIDATION ERROR

Field: title
Code: TITLE_REQUIRED
Message: Title is required and cannot be omitted.
Constraint: Title must be provided for every task.
Received: [null | undefined]

Fix: Provide a title between 1 and 200 characters.
```

**TITLE_EMPTY**:
```
VALIDATION ERROR

Field: title
Code: TITLE_EMPTY
Message: Title cannot be empty or only whitespace.
Constraint: Title must have at least 1 non-whitespace character.
Received: "[actual value]"

Fix: Provide a meaningful title with visible characters.
```

**TITLE_TOO_LONG**:
```
VALIDATION ERROR

Field: title
Code: TITLE_TOO_LONG
Message: Title exceeds maximum length of 200 characters.
Constraint: Title must be 200 characters or fewer.
Received: [length] characters

Fix: Shorten the title to 200 characters or fewer.
```

#### Description Errors

**DESCRIPTION_TOO_LONG**:
```
VALIDATION ERROR

Field: description
Code: DESCRIPTION_TOO_LONG
Message: Description exceeds maximum length of 1000 characters.
Constraint: Description must be 1000 characters or fewer.
Received: [length] characters

Fix: Shorten the description to 1000 characters or fewer.
```

**DESCRIPTION_INVALID_TYPE**:
```
VALIDATION ERROR

Field: description
Code: DESCRIPTION_INVALID_TYPE
Message: Description must be a string or null.
Constraint: Description type must be string when provided.
Received: [actual type]

Fix: Provide description as a string or omit it entirely.
```

#### Status Errors

**STATUS_REQUIRED**:
```
VALIDATION ERROR

Field: status
Code: STATUS_REQUIRED
Message: Status is required.
Constraint: Status must be provided or default applied.
Received: [null | undefined]

Fix: Provide status as "pending" or "completed".
```

**STATUS_INVALID**:
```
VALIDATION ERROR

Field: status
Code: STATUS_INVALID
Message: Status must be "pending" or "completed".
Constraint: Only two status values are allowed in Phase I.
Received: "[actual value]"

Fix: Use exactly "pending" or "completed" (case-sensitive).
```

### Aggregate Error Response

When multiple validations fail:
```
VALIDATION FAILED

Operation: [Add | Update | Mark Complete]
Errors Found: [count]

1. [Field: title]
   Code: TITLE_EMPTY
   Message: Title cannot be empty or only whitespace.

2. [Field: status]
   Code: STATUS_INVALID
   Message: Status must be "pending" or "completed".

All errors must be resolved before the operation can proceed.
```

## Integration with Agents

### With task-domain-enforcer

Primary enforcement point:
- Apply all validation rules at domain boundary
- Reject invalid entities before creation
- Ensure domain invariants are maintained

### With in-memory-state-manager

State protection:
- Validate before any state modification
- Prevent invalid data from entering state
- Maintain state consistency

### With cli-interface

User input validation:
- Validate user-provided values
- Display clear error messages
- Guide users toward valid input

### With spec-driven-architect

Spec compliance:
- Validation rules derived from spec
- Constraints match spec definitions
- Changes require spec updates first

## Validation Summary Table

| Field | Required | Type | Min | Max | Allowed Values |
|-------|----------|------|-----|-----|----------------|
| title | Yes | string | 1 | 200 | Any non-empty string |
| description | No | string/null | 0 | 1000 | Any string or null |
| status | Yes* | string | - | - | "pending", "completed" |

*Default: "pending" when not provided on creation

## Phase I Scope Note

These validation rules are specific to Phase I:
- Status values are limited to "pending" and "completed"
- Future phases may add: "in_progress", "blocked", "archived"
- Validation rules will evolve with spec updates
- This skill reads current rules and adapts accordingly

## Validation Checklist

Before accepting any task data:

- [ ] Title is present
- [ ] Title is a string
- [ ] Title is not empty/whitespace-only
- [ ] Title is 200 characters or fewer
- [ ] Description (if provided) is a string
- [ ] Description (if provided) is 1000 characters or fewer
- [ ] Status is present or default applied
- [ ] Status is exactly "pending" or "completed"

## Guiding Principle

> "Invalid data never enters the system. Every task is validated at the boundary, every field is checked against its constraints, and every violation is reported clearly. The validation rules are the contract—honor them without exception."

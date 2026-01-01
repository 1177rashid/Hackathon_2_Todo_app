# Task Validator

## Purpose

This skill provides a dedicated validation layer for Task entity inputs in the Phase I Todo application. It validates all task data against defined rules and returns structured results that can be consumed by any agent in the system.

The skill is designed to:
- Validate task inputs before any state modification
- Enforce Phase I domain rules consistently
- Return machine-readable validation results
- Detect and prevent duplicate tasks
- Serve as a single source of validation truth

## Validation Rules

### Rule 1: Title Validation

| Check | Constraint | Error Message |
|-------|------------|---------------|
| Presence | Required | "Title is required" |
| Type | Must be string | "Title must be a string" |
| Empty | Cannot be empty/whitespace | "Title cannot be empty" |
| Min Length | At least 1 character | "Title must be at least 1 character" |
| Max Length | At most 200 characters | "Title cannot exceed 200 characters" |

**Validation Logic**:
```
validate_title(title):
  if title is null or undefined:
    return error("Title is required")
  if typeof title !== string:
    return error("Title must be a string")
  if title.trim().length === 0:
    return error("Title cannot be empty")
  if title.trim().length > 200:
    return error("Title cannot exceed 200 characters")
  return valid
```

### Rule 2: Description Validation

| Check | Constraint | Error Message |
|-------|------------|---------------|
| Presence | Optional (can be null) | N/A |
| Type | Must be string when provided | "Description must be a string" |
| Max Length | At most 1000 characters | "Description cannot exceed 1000 characters" |

**Validation Logic**:
```
validate_description(description):
  if description is null or undefined:
    return valid (optional field)
  if typeof description !== string:
    return error("Description must be a string")
  if description.length > 1000:
    return error("Description cannot exceed 1000 characters")
  return valid
```

### Rule 3: Duplicate Detection

| Check | Constraint | Error Message |
|-------|------------|---------------|
| Title Uniqueness | No exact title match | "A task with this title already exists" |
| Case Sensitivity | Case-insensitive match | "A task with this title already exists (case-insensitive)" |

**Validation Logic**:
```
validate_no_duplicate(title, existing_tasks, exclude_id?):
  normalized_title = title.trim().toLowerCase()
  for task in existing_tasks:
    if task.id === exclude_id:
      continue (skip self on updates)
    if task.title.trim().toLowerCase() === normalized_title:
      return error("A task with this title already exists")
  return valid
```

### Rule Summary Table

| Field | Required | Type | Min | Max | Unique |
|-------|----------|------|-----|-----|--------|
| title | Yes | string | 1 | 200 | Yes (case-insensitive) |
| description | No | string | 0 | 1000 | No |

## Input/Output Structure

### Input Format

The validator accepts a structured input object:

```
ValidationInput = {
  task: {
    title: String | null,
    description: String | null
  },
  context: {
    operation: "add" | "update",
    existing_tasks: List<Task>,
    exclude_id: Integer | null    // For updates, exclude self from duplicate check
  }
}
```

**Simplified Input** (for basic validation without duplicate check):
```
ValidationInput = {
  task: {
    title: String | null,
    description: String | null
  }
}
```

### Output Format

The validator returns a structured result:

**Success (Valid)**:
```
{
  valid: true,
  errors: []
}
```

**Failure (Invalid)**:
```
{
  valid: false,
  errors: [
    "Title is required",
    "Description cannot exceed 1000 characters"
  ]
}
```

### Detailed Output Format (Optional)

For agents needing more context:

```
{
  valid: false,
  errors: [
    {
      field: "title",
      code: "REQUIRED",
      message: "Title is required"
    },
    {
      field: "description",
      code: "MAX_LENGTH",
      message: "Description cannot exceed 1000 characters",
      constraint: 1000,
      actual: 1247
    }
  ],
  summary: {
    total_errors: 2,
    fields_with_errors: ["title", "description"]
  }
}
```

## Validation Modes

### Mode 1: Add Task Validation

Validates all fields plus duplicate check:

```
Input:
{
  task: { title: "Buy groceries", description: null },
  context: {
    operation: "add",
    existing_tasks: [existing task list]
  }
}

Checks Applied:
- Title presence ✓
- Title type ✓
- Title length ✓
- Description type (if provided) ✓
- Description length (if provided) ✓
- Duplicate detection ✓
```

### Mode 2: Update Task Validation

Validates provided fields, excludes self from duplicate check:

```
Input:
{
  task: { title: "Buy groceries today", description: null },
  context: {
    operation: "update",
    existing_tasks: [existing task list],
    exclude_id: 5
  }
}

Checks Applied:
- Title presence (if in payload) ✓
- Title type (if in payload) ✓
- Title length (if in payload) ✓
- Description type (if in payload) ✓
- Description length (if in payload) ✓
- Duplicate detection (excluding task 5) ✓
```

### Mode 3: Field-Only Validation

Validates individual fields without context:

```
Input:
{
  task: { title: "Buy groceries" }
}

Checks Applied:
- Title presence ✓
- Title type ✓
- Title length ✓
- No duplicate check (no context)
```

## Error Code Reference

| Code | Field | Message Template |
|------|-------|------------------|
| `REQUIRED` | title | "Title is required" |
| `INVALID_TYPE` | title | "Title must be a string" |
| `EMPTY` | title | "Title cannot be empty" |
| `MIN_LENGTH` | title | "Title must be at least 1 character" |
| `MAX_LENGTH` | title | "Title cannot exceed 200 characters" |
| `INVALID_TYPE` | description | "Description must be a string" |
| `MAX_LENGTH` | description | "Description cannot exceed 1000 characters" |
| `DUPLICATE` | title | "A task with this title already exists" |

## Integration with Agents

### With task-domain-enforcer

Primary domain validation:
```
Flow:
1. task-domain-enforcer receives task data
2. Calls task-validator with task input
3. Receives validation result
4. If valid: proceed with domain logic
5. If invalid: return errors, block operation
```

### With in-memory-state-manager

State protection layer:
```
Flow:
1. in-memory-state-manager receives CRUD request
2. Before modifying state, calls task-validator
3. Passes existing_tasks for duplicate detection
4. If valid: execute state operation
5. If invalid: return validation errors
```

### With cli-interface

User input validation:
```
Flow:
1. cli-interface collects user input
2. Calls task-validator for immediate feedback
3. If valid: pass to state manager
4. If invalid: display errors, prompt retry
```

### With spec-driven-architect

Spec compliance verification:
```
Flow:
1. Architect reviews validation rules
2. Confirms rules match spec definitions
3. Ensures validator enforces spec constraints
```

## Validation Pipeline

### Execution Order

Validations run in sequence, collecting all errors:

```
1. Title Validation
   ├── Check presence
   ├── Check type
   ├── Check not empty
   └── Check length

2. Description Validation
   ├── Check type (if provided)
   └── Check length (if provided)

3. Duplicate Detection (if context provided)
   └── Check title uniqueness

4. Aggregate Results
   └── Return { valid, errors }
```

### Early Exit vs. Full Collection

**Default: Full Collection**
- Run all validations
- Collect all errors
- Return complete error list
- User sees all issues at once

**Optional: Early Exit**
- Stop on first error
- Return single error
- Faster execution
- User fixes one issue at a time

## Usage Examples

### Example 1: Valid Add Task

```
Input:
{
  task: {
    title: "Complete project report",
    description: "Finish Q4 summary by Friday"
  },
  context: {
    operation: "add",
    existing_tasks: []
  }
}

Output:
{
  valid: true,
  errors: []
}
```

### Example 2: Missing Title

```
Input:
{
  task: {
    title: null,
    description: "Some description"
  }
}

Output:
{
  valid: false,
  errors: ["Title is required"]
}
```

### Example 3: Multiple Errors

```
Input:
{
  task: {
    title: "",
    description: "[1001 character string...]"
  }
}

Output:
{
  valid: false,
  errors: [
    "Title cannot be empty",
    "Description cannot exceed 1000 characters"
  ]
}
```

### Example 4: Duplicate Title

```
Input:
{
  task: {
    title: "Buy groceries",
    description: null
  },
  context: {
    operation: "add",
    existing_tasks: [
      { id: 1, title: "Buy Groceries", status: "pending" }
    ]
  }
}

Output:
{
  valid: false,
  errors: ["A task with this title already exists"]
}
```

### Example 5: Valid Update (Self-Exclusion)

```
Input:
{
  task: {
    title: "Buy groceries today",
    description: null
  },
  context: {
    operation: "update",
    existing_tasks: [
      { id: 1, title: "Buy groceries", status: "pending" }
    ],
    exclude_id: 1
  }
}

Output:
{
  valid: true,
  errors: []
}
```

## Guiding Principle

> "Validate once, validate completely, validate before state changes. Every task input passes through this single validator—no exceptions, no shortcuts. Invalid data is caught here, not in the state layer."

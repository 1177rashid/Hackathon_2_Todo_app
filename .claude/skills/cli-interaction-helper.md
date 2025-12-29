# CLI Interaction Helper

## Purpose

This skill provides standardized patterns for command-line interface interactions in the Phase I Todo application. It defines how to display information, prompt for user input, show feedback messages, and navigate menus—ensuring a consistent, user-friendly CLI experience.

The skill is designed to:
- Standardize CLI output formatting across all operations
- Provide clear, accessible user prompts
- Display meaningful success and error feedback
- Support intuitive menu-based navigation
- Maintain consistency in all user-facing interactions

## Supported CLI Interactions

### 1. Main Menu Display

The entry point for user interaction:

```
====================================
         TODO APPLICATION
====================================

  [1] View Tasks
  [2] Add Task
  [3] Update Task
  [4] Delete Task
  [5] Mark Complete
  [0] Exit

====================================
Enter choice: _
```

### 2. Task List Display

Shows all tasks with status indicators:

```
====================================
           YOUR TASKS
====================================

  ID   Status      Title
  --   ------      -----
  1    [ ]         Buy groceries
  2    [x]         Complete project report
  3    [ ]         Call dentist
  4    [ ]         Review pull request

====================================
Total: 4 tasks (1 completed, 3 pending)
```

**Status Indicators**:
- `[ ]` - Pending task
- `[x]` - Completed task

### 3. Task Detail View

Shows full details of a single task:

```
====================================
          TASK DETAILS
====================================

  ID:          3
  Title:       Call dentist
  Description: Schedule annual checkup appointment
  Status:      Pending [ ]

====================================
```

### 4. Empty State Display

When no tasks exist:

```
====================================
           YOUR TASKS
====================================

  No tasks found.

  Use option [2] to add your first task.

====================================
```

### 5. Add Task Flow

Sequential prompts for creating a task:

```
====================================
           ADD NEW TASK
====================================

Enter title (required, max 200 chars):
> _

Enter description (optional, max 1000 chars):
> _

```

### 6. Update Task Flow

Prompts for modifying an existing task:

```
====================================
          UPDATE TASK
====================================

Enter task ID to update: _

Current values:
  Title:       Buy groceries
  Description: Weekly shopping list

Enter new title (or press Enter to keep current):
> _

Enter new description (or press Enter to keep current):
> _

```

### 7. Delete Task Flow

Confirmation before deletion:

```
====================================
          DELETE TASK
====================================

Enter task ID to delete: _

You are about to delete:
  ID:    1
  Title: Buy groceries

Are you sure? (y/n): _
```

### 8. Mark Complete Flow

Simple completion marking:

```
====================================
        MARK TASK COMPLETE
====================================

Enter task ID to mark complete: _

Task marked complete:
  ID:    2
  Title: Complete project report
  Status: [x] Completed

```

## How to Prompt the User

### Prompt Principles

1. **Be Clear**: State exactly what input is expected
2. **Show Constraints**: Indicate required fields and limits
3. **Provide Context**: Show current values when updating
4. **Use Consistent Format**: Same prompt style throughout

### Prompt Patterns

#### Text Input Prompt
```
Enter [field name] ([required/optional], max [N] chars):
> _
```

#### Numeric Input Prompt
```
Enter [item] ID: _
```

#### Choice Prompt
```
Enter choice: _
```

#### Confirmation Prompt
```
Are you sure? (y/n): _
```

#### Optional Field Prompt
```
Enter [field] (or press Enter to skip):
> _
```

#### Update Field Prompt
```
Enter new [field] (or press Enter to keep current):
> _
```

### Input Validation Feedback

When user input fails validation, show inline feedback:

```
Enter title (required, max 200 chars):
>

Error: Title cannot be empty. Please enter a title.

Enter title (required, max 200 chars):
> _
```

```
Enter task ID to update: abc

Error: Invalid ID. Please enter a number.

Enter task ID to update: _
```

## How to Display Feedback

### Success Messages

Use clear confirmation with details:

**Task Added**:
```
SUCCESS: Task added successfully.

  ID:    5
  Title: New task title

Returning to main menu...
```

**Task Updated**:
```
SUCCESS: Task updated successfully.

  ID:    3
  Title: Updated title

Returning to main menu...
```

**Task Deleted**:
```
SUCCESS: Task deleted successfully.

  Deleted ID: 2

Returning to main menu...
```

**Task Completed**:
```
SUCCESS: Task marked as complete.

  ID:     4
  Title:  Review pull request
  Status: [x] Completed

Returning to main menu...
```

### Error Messages

Provide clear error with guidance:

**Validation Error**:
```
ERROR: Invalid input.

  Field: title
  Issue: Title exceeds 200 characters (received: 245)

Please try again with a shorter title.
```

**Not Found Error**:
```
ERROR: Task not found.

  Requested ID: 99
  Issue: No task exists with this ID.

Use option [1] to view available tasks.
```

**Operation Error**:
```
ERROR: Operation failed.

  Operation: Delete
  Issue: Cannot delete task that doesn't exist.

Please verify the task ID and try again.
```

### Warning Messages

Alert without blocking:

```
WARNING: No changes detected.

  The values you entered match the current values.
  Task was not modified.

Returning to main menu...
```

### Informational Messages

Neutral status updates:

```
INFO: Operation cancelled.

  No changes were made.

Returning to main menu...
```

## Menu Navigation

### Menu Structure

```
Main Menu
├── [1] View Tasks → Task List Display
├── [2] Add Task → Add Task Flow → Success/Error
├── [3] Update Task → Update Task Flow → Success/Error
├── [4] Delete Task → Delete Task Flow → Success/Error
├── [5] Mark Complete → Mark Complete Flow → Success/Error
└── [0] Exit → Goodbye Message
```

### Navigation Feedback

**Entering a Section**:
```
====================================
           ADD NEW TASK
====================================
```

**Returning to Menu**:
```
Returning to main menu...

[Menu displays again]
```

**Exit Application**:
```
====================================
  Thank you for using Todo App!
  Goodbye.
====================================
```

### Invalid Menu Choice

```
Enter choice: 9

Invalid choice. Please enter a number between 0 and 5.

Enter choice: _
```

## Display Formatting Guidelines

### Borders and Separators

Use consistent visual boundaries:
```
====================================  (36 chars, section header)
------------------------------------  (36 chars, subsection)
```

### Alignment

- Left-align text content
- Right-align numeric IDs in columns
- Consistent indentation (2 spaces)

### Column Layout for Task Lists

```
  ID   Status      Title
  --   ------      -----
  1    [ ]         Short title
  12   [x]         Another task title here
  123  [ ]         Yet another task
```

### Status Indicators

| Status | Indicator | Display |
|--------|-----------|---------|
| Pending | `[ ]` | Empty checkbox |
| Completed | `[x]` | Checked checkbox |

### Message Prefixes

| Type | Prefix | Use Case |
|------|--------|----------|
| Success | `SUCCESS:` | Operation completed |
| Error | `ERROR:` | Operation failed |
| Warning | `WARNING:` | Non-blocking issue |
| Info | `INFO:` | Neutral information |

## Integration with Agents

### With cli-interface Agent

Primary consumer of this skill:
- Implements all display patterns
- Handles all user prompts
- Formats all feedback messages

### With in-memory-state-manager

Data source for displays:
- Retrieves task data for list display
- Provides task details for detail view
- Returns operation results for feedback

### With task-validation-rules

Validation feedback:
- Receives validation errors
- Formats errors for user display
- Guides user to correct input

### With id-integrity-manager

ID-related feedback:
- Displays ID errors clearly
- Guides user to valid IDs
- Shows available task IDs when needed

## Accessibility Considerations

### Clear Language
- Use simple, direct language
- Avoid jargon or technical terms
- Explain what user needs to do

### Consistent Patterns
- Same prompt format throughout
- Same feedback format throughout
- Predictable navigation

### Error Recovery
- Always explain what went wrong
- Always suggest how to fix it
- Never leave user stuck

## CLI Output Templates

### Template: Section Header
```
====================================
         [SECTION TITLE]
====================================
```

### Template: Success Feedback
```
SUCCESS: [Action] successfully.

  [Key]: [Value]
  [Key]: [Value]

Returning to main menu...
```

### Template: Error Feedback
```
ERROR: [Brief error description].

  [Field/Item]: [Specific value]
  Issue: [What went wrong]

[Guidance on how to fix]
```

### Template: Prompt
```
Enter [what is needed] ([constraints]):
> _
```

### Template: Confirmation
```
You are about to [action]:
  [Details of what will happen]

Are you sure? (y/n): _
```

## Guiding Principle

> "The CLI is the user's window into the application. Every prompt should be clear, every response should be helpful, and every error should guide toward resolution. Consistency builds familiarity; clarity builds trust."

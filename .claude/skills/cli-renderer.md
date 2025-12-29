# CLI Renderer

## Purpose

This skill serves as the presentation layer for the Phase I Todo application. It handles all rendering of output to the terminal and collection of input from the user, providing a clean separation between display logic and business logic.

The skill is designed to:
- Render all visual elements to the command line
- Display menus, prompts, and feedback consistently
- Collect and structure user input for downstream agents
- Format task data for human-readable display
- Translate operation results into user-friendly messages

## CLI Responsibilities

### 1. Menu Rendering

Display the main application menu:

```
render_main_menu() → void

Output:
╔════════════════════════════════════╗
║         TODO APPLICATION           ║
╠════════════════════════════════════╣
║                                    ║
║   [1] View Tasks                   ║
║   [2] Add Task                     ║
║   [3] Update Task                  ║
║   [4] Delete Task                  ║
║   [5] Mark Complete                ║
║   [0] Exit                         ║
║                                    ║
╚════════════════════════════════════╝

Enter your choice: _
```

### 2. Task List Rendering

Display all tasks with status indicators:

```
render_task_list(tasks: List<Task>, summary: Summary) → void

Output:
┌────────────────────────────────────┐
│           YOUR TASKS               │
├────┬────────┬──────────────────────┤
│ ID │ Status │ Title                │
├────┼────────┼──────────────────────┤
│  1 │ [ ]    │ Buy groceries        │
│  2 │ [x]    │ Complete report      │
│  3 │ [ ]    │ Call dentist         │
└────┴────────┴──────────────────────┘

Total: 3 tasks | Completed: 1 | Pending: 2
```

**Status Indicators**:
| Status | Indicator | Meaning |
|--------|-----------|---------|
| pending | `[ ]` | Task not completed |
| completed | `[x]` | Task completed |

### 3. Task Detail Rendering

Display single task with full details:

```
render_task_detail(task: Task) → void

Output:
┌────────────────────────────────────┐
│          TASK DETAILS              │
├────────────────────────────────────┤
│ ID:          3                     │
│ Title:       Call dentist          │
│ Description: Schedule checkup      │
│ Status:      [ ] Pending           │
└────────────────────────────────────┘
```

### 4. Prompt Rendering

Display input prompts to the user:

```
render_prompt(prompt_type: String, options?: Object) → void

Prompt Types:
- text_input: Free text entry
- id_input: Numeric ID entry
- confirmation: Yes/No choice
- menu_choice: Numeric menu selection
```

**Text Input Prompt**:
```
Enter task title (required, max 200 chars):
> _
```

**ID Input Prompt**:
```
Enter task ID: _
```

**Confirmation Prompt**:
```
Are you sure you want to delete this task? (y/n): _
```

**Optional Field Prompt**:
```
Enter description (optional, press Enter to skip):
> _
```

### 5. Success Message Rendering

Display operation success feedback:

```
render_success(operation: String, data: Object) → void

Output Examples:

[Add Success]
✓ SUCCESS: Task created successfully.
  ID:    4
  Title: New task title

[Update Success]
✓ SUCCESS: Task updated successfully.
  ID:    2
  Title: Updated title

[Delete Success]
✓ SUCCESS: Task deleted.
  Removed: "Old task title"

[Complete Success]
✓ SUCCESS: Task marked as complete.
  ID:    3
  Title: Call dentist
  Status: [x] Completed
```

### 6. Error Message Rendering

Display operation failures and validation errors:

```
render_error(error_type: String, details: Object) → void

Output Examples:

[Validation Error]
✗ ERROR: Validation failed.
  • Title is required
  • Description cannot exceed 1000 characters

[Not Found Error]
✗ ERROR: Task not found.
  No task exists with ID: 99

[Operation Error]
✗ ERROR: Operation failed.
  Could not delete task. Please try again.
```

### 7. Warning Message Rendering

Display non-blocking warnings:

```
render_warning(message: String) → void

Output:
⚠ WARNING: No changes detected.
  The task was not modified.
```

### 8. Empty State Rendering

Display when no tasks exist:

```
render_empty_state() → void

Output:
┌────────────────────────────────────┐
│           YOUR TASKS               │
├────────────────────────────────────┤
│                                    │
│     No tasks found.                │
│                                    │
│     Use [2] to add your first      │
│     task.                          │
│                                    │
└────────────────────────────────────┘
```

## Input/Output Structure

### Input Collection

The renderer collects user input and returns structured data:

**Menu Choice Input**:
```
collect_menu_choice() → RendererInput

Returns:
{
  type: "menu_choice",
  value: Integer (0-5),
  raw: String
}
```

**Text Input**:
```
collect_text_input(field: String, required: Boolean) → RendererInput

Returns:
{
  type: "text_input",
  field: "title" | "description",
  value: String | null,
  raw: String
}
```

**ID Input**:
```
collect_id_input() → RendererInput

Returns:
{
  type: "id_input",
  value: Integer | null,
  raw: String,
  valid: Boolean
}
```

**Confirmation Input**:
```
collect_confirmation() → RendererInput

Returns:
{
  type: "confirmation",
  value: Boolean,
  raw: String ("y" | "n")
}
```

### Output Rendering

The renderer accepts structured data for display:

**Task List Output**:
```
Input:
{
  type: "task_list",
  tasks: [
    { id: 1, title: "...", description: "...", status: "pending" },
    { id: 2, title: "...", description: null, status: "completed" }
  ],
  summary: {
    total: 2,
    pending: 1,
    completed: 1
  }
}
```

**Success Output**:
```
Input:
{
  type: "success",
  operation: "add" | "update" | "delete" | "complete",
  task: { id, title, status },
  message: "Task created successfully."
}
```

**Error Output**:
```
Input:
{
  type: "error",
  code: "VALIDATION_ERROR" | "NOT_FOUND" | "OPERATION_FAILED",
  errors: ["Error message 1", "Error message 2"],
  context: { field: "title", task_id: 99 }
}
```

## Rendering Specifications

### Visual Elements

| Element | Character | Usage |
|---------|-----------|-------|
| Box top-left | `┌` or `╔` | Section headers |
| Box top-right | `┐` or `╗` | Section headers |
| Box bottom-left | `└` or `╚` | Section footers |
| Box bottom-right | `┘` or `╝` | Section footers |
| Horizontal line | `─` or `═` | Borders |
| Vertical line | `│` or `║` | Borders |
| Success icon | `✓` | Success messages |
| Error icon | `✗` | Error messages |
| Warning icon | `⚠` | Warning messages |
| Pending checkbox | `[ ]` | Incomplete task |
| Complete checkbox | `[x]` | Completed task |

### Text Formatting

| Style | Usage | Example |
|-------|-------|---------|
| UPPERCASE | Section headers | `YOUR TASKS` |
| Title Case | Menu items | `View Tasks` |
| lowercase | Error details | `title is required` |
| Indented (2 spaces) | List items, details | `  ID: 1` |

### Width Constraints

| Element | Width | Notes |
|---------|-------|-------|
| Box width | 36-40 chars | Consistent borders |
| Title display | 20 chars max | Truncate with `...` |
| ID column | 4 chars | Right-aligned |
| Status column | 8 chars | Centered |

### Truncation Rules

When content exceeds display width:
```
Full:      "This is a very long task title that exceeds the limit"
Truncated: "This is a very long t..."
```

## Interaction Flows

### Flow 1: View Tasks

```
User selects [1]
       │
       ▼
render_task_list(tasks, summary)
       │
       ▼
[Display task table]
       │
       ▼
render_prompt("continue")
       │
       ▼
[Return to main menu]
```

### Flow 2: Add Task

```
User selects [2]
       │
       ▼
render_prompt("text_input", {field: "title", required: true})
       │
       ▼
collect_text_input("title", true) → title
       │
       ▼
render_prompt("text_input", {field: "description", required: false})
       │
       ▼
collect_text_input("description", false) → description
       │
       ▼
[Return structured input to calling agent]
       │
       ▼
[Agent processes, returns result]
       │
       ▼
render_success("add", task) OR render_error("validation", errors)
       │
       ▼
[Return to main menu]
```

### Flow 3: Update Task

```
User selects [3]
       │
       ▼
render_task_list(tasks, summary)  // Show available tasks
       │
       ▼
render_prompt("id_input")
       │
       ▼
collect_id_input() → task_id
       │
       ▼
render_task_detail(current_task)  // Show current values
       │
       ▼
render_prompt("text_input", {field: "title", current: task.title})
       │
       ▼
collect_text_input("title", false) → new_title
       │
       ▼
render_prompt("text_input", {field: "description", current: task.description})
       │
       ▼
collect_text_input("description", false) → new_description
       │
       ▼
[Return structured input to calling agent]
       │
       ▼
render_success("update", task) OR render_error(...)
```

### Flow 4: Delete Task

```
User selects [4]
       │
       ▼
render_task_list(tasks, summary)
       │
       ▼
render_prompt("id_input")
       │
       ▼
collect_id_input() → task_id
       │
       ▼
render_task_detail(task)  // Show what will be deleted
       │
       ▼
render_prompt("confirmation", {action: "delete"})
       │
       ▼
collect_confirmation() → confirmed
       │
       ▼
if confirmed: [Proceed] else: [Cancel, return to menu]
       │
       ▼
render_success("delete", task) OR render_error(...)
```

### Flow 5: Mark Complete

```
User selects [5]
       │
       ▼
render_task_list(tasks, summary, {filter: "pending"})  // Show pending only
       │
       ▼
render_prompt("id_input")
       │
       ▼
collect_id_input() → task_id
       │
       ▼
[Agent processes completion]
       │
       ▼
render_success("complete", task) OR render_error(...)
```

## Integration with Agents

### With cli-interface Agent

Primary consumer:
```
cli-interface owns the interaction loop:
1. Calls renderer to display menu
2. Calls renderer to collect input
3. Passes structured input to state/domain agents
4. Receives operation results
5. Calls renderer to display feedback
6. Loops back to menu
```

### With in-memory-state-manager

Data provider:
```
Flow:
1. cli-interface requests task list
2. in-memory-state-manager returns task data
3. cli-interface passes data to renderer
4. Renderer formats and displays

Data Format Expected:
{
  tasks: List<Task>,
  summary: { total, pending, completed }
}
```

### With task-domain-enforcer

Validation feedback:
```
Flow:
1. Renderer collects user input
2. cli-interface passes to domain enforcer
3. Domain enforcer validates, returns result
4. If errors: renderer displays validation errors
5. If valid: proceed with operation

Error Format Expected:
{
  valid: false,
  errors: ["error 1", "error 2"]
}
```

### With task-validator

Input validation display:
```
Flow:
1. Renderer collects raw input
2. Validator checks input
3. Renderer displays any validation errors inline
4. User corrects and re-enters
```

## Separation of Concerns

### Renderer Does:
- Display formatted output
- Collect raw user input
- Structure input for agents
- Format feedback messages
- Handle display truncation
- Manage visual consistency

### Renderer Does NOT:
- Validate business rules
- Modify task state
- Make decisions about data
- Store any state
- Implement business logic
- Access data directly

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| box_style | "single" | "single" or "double" borders |
| max_title_display | 20 | Chars before truncation |
| show_descriptions | false | Show descriptions in list |
| color_enabled | false | ANSI color support (future) |

## Guiding Principle

> "The renderer displays, it does not decide. It collects input, it does not validate. It formats output, it does not generate. Every visual element is consistent, every prompt is clear, and every response is structured for downstream consumption."

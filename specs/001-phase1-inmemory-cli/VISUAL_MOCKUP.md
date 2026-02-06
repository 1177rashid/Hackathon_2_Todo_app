# Visual Mockup - Rich CLI Interface

This document shows the actual appearance of the Todo application with Rich library enhancements.

## Application Startup

```
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│     ████████╗ ██████╗ ██████╗  ██████╗                      │
│     ╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗                     │
│        ██║   ██║   ██║██║  ██║██║   ██║                     │
│        ██║   ██║   ██║██║  ██║██║   ██║                     │
│        ██║   ╚██████╔╝██████╔╝╚██████╔╝                     │
│        ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝                      │
│                                                               │
│           📝 Organize Your Life, One Task at a Time 📝        │
│                        Version 1.0.0                          │
└───────────────────────────────────────────────────────────────┘

Colors: Title in bold magenta, tagline in cyan, border in cyan
```

## Main Menu

```
┌─────────────────────── TODO APP MENU ────────────────────────┐
│                                                               │
│   ➕ 1. Add Task         ✏️  3. Update Task                  │
│   📋 2. View Tasks       ❌ 4. Delete Task                   │
│   ✅ 5. Mark Complete   🔄 6. Mark Incomplete                │
│   🚪 7. Exit                                                  │
│                                                               │
└───────────────────────────────────────────────────────────────┘

 👉 Enter your choice: _

Colors:
- Title "TODO APP MENU" in bold magenta
- Options 1-6 in bold white
- Exit option in bold yellow
- Border in cyan
- Prompt in bold cyan
```

## View Tasks - With Data

```
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃  ID  ┃         Title         ┃     Description      ┃   Status    ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│  1   │  Buy groceries        │  Milk, eggs, bread   │ ✅ Done     │
│  2   │  Finish project       │  Complete Phase 1... │ ⏳ Pending  │
│  3   │  Call dentist         │                      │ ⏳ Pending  │
└──────┴───────────────────────┴──────────────────────┴─────────────┘

                        📊 Total: 3 task(s)

Colors:
- Table title "YOUR TASKS" in bold magenta
- Header row in bold magenta
- ID column in bold white
- Title column in bold cyan
- Description in white
- "✅ Done" in bold green
- "⏳ Pending" in bold yellow
- Border in cyan
- Total count in bold white
```

## View Tasks - Empty State

```
┌─────────────────────── YOUR TASKS ───────────────────────┐
│                                                           │
│        📭 No tasks found!                                 │
│        Add your first task to get started.               │
│                                                           │
└───────────────────────────────────────────────────────────┘

Colors:
- Title in bold magenta
- "No tasks found!" in yellow
- Help text in cyan
- Border in cyan
```

## Add Task Operation

```
┌────────────────────── ADD NEW TASK ──────────────────────┐
│  ➕ Creating a new task                                   │
└───────────────────────────────────────────────────────────┘

 📝 Enter task title: Buy groceries

 📄 Enter task description (optional): Milk, eggs, and bread

┌───────────────────────────────────────────────────────────┐
│  ✅ Task created with ID: 1                               │
└───────────────────────────────────────────────────────────┘

Colors:
- Header panel border in cyan
- Prompts in bold cyan with emojis
- Success panel border in green
- Success message in bold green
```

## Update Task Operation

```
┌────────────────────── UPDATE TASK ───────────────────────┐
│  ✏️  Modify an existing task                             │
└───────────────────────────────────────────────────────────┘

 🔢 Enter task ID: 1

Current Values:
┌───────────────────────────────────────────────────────────┐
│  Title: Buy groceries                                     │
│  Description: Milk and bread                              │
└───────────────────────────────────────────────────────────┘

 📝 Enter new title (or press Enter to keep current): Buy groceries and vegetables

 📄 Enter new description (or press Enter to keep current): Milk, eggs, bread, carrots

┌───────────────────────────────────────────────────────────┐
│  ✅ Task 1 updated successfully!                          │
└───────────────────────────────────────────────────────────┘

Colors:
- Header panel border in cyan
- Current values label in bold yellow
- Current values panel border in yellow
- Field labels in cyan
- Prompts in bold cyan
- Success panel border in green
```

## Delete Task Operation

```
┌────────────────────── DELETE TASK ───────────────────────┐
│  ❌ Remove a task permanently                            │
└───────────────────────────────────────────────────────────┘

 🔢 Enter task ID: 2

┌───────────────────────────────────────────────────────────┐
│  ✅ Task 2 deleted successfully!                          │
└───────────────────────────────────────────────────────────┘

Colors:
- Header panel border in cyan
- Prompt in bold cyan
- Success panel border in green
```

## Mark Complete Operation

```
┌───────────────── MARK TASK COMPLETE ─────────────────────┐
│  ✅ Mark task as completed                               │
└───────────────────────────────────────────────────────────┘

 🔢 Enter task ID: 3

┌───────────────────────────────────────────────────────────┐
│  ✅ Task 3 marked as complete!                            │
└───────────────────────────────────────────────────────────┘

Colors:
- Header panel border in cyan
- Prompt in bold cyan
- Success panel border in green
```

## Mark Incomplete Operation

```
┌──────────────── MARK TASK INCOMPLETE ────────────────────┐
│  🔄 Mark task as incomplete                              │
└───────────────────────────────────────────────────────────┘

 🔢 Enter task ID: 1

┌───────────────────────────────────────────────────────────┐
│  ✅ Task 1 marked as incomplete!                          │
└───────────────────────────────────────────────────────────┘

Colors:
- Header panel border in cyan
- Prompt in bold cyan
- Success panel border in green
```

## Error Messages

### Task Not Found
```
┌────────────────────────── ERROR ─────────────────────────┐
│  ❌ Task with ID 99 not found.                           │
└───────────────────────────────────────────────────────────┘

Colors: Border and message in bold red
```

### Invalid Input
```
┌────────────────────────── ERROR ─────────────────────────┐
│  ❌ Please enter a valid number.                         │
└───────────────────────────────────────────────────────────┘

Colors: Border and message in bold red
```

### Empty Title
```
┌────────────────────────── ERROR ─────────────────────────┐
│  ❌ Title cannot be empty or whitespace-only.            │
└───────────────────────────────────────────────────────────┘

Colors: Border and message in bold red
```

## Exit Message

```
┌───────────────────────────────────────────────────────────┐
│  👋 Thank you for using Todo App!                        │
│  Stay organized and productive!                          │
└───────────────────────────────────────────────────────────┘

Colors:
- Thank you message in bold cyan
- Tagline in yellow
- Border in magenta
```

## Complete User Flow Example

```
[STARTUP - Welcome Banner appears]

┌───────────────────────────────────────────────────────────┐
│     ████████╗ ██████╗ ██████╗  ██████╗                  │
│     (... ASCII art in bold magenta ...)                  │
│     📝 Organize Your Life, One Task at a Time 📝         │
└───────────────────────────────────────────────────────────┘

[MENU appears]

┌─────────────────────── TODO APP MENU ────────────────────┐
│   ➕ 1. Add Task         ✏️  3. Update Task             │
│   📋 2. View Tasks       ❌ 4. Delete Task              │
│   ✅ 5. Mark Complete   🔄 6. Mark Incomplete           │
│   🚪 7. Exit                                             │
└───────────────────────────────────────────────────────────┘

 👉 Enter your choice: 1

[ADD TASK screen]

┌────────────────────── ADD NEW TASK ──────────────────────┐
│  ➕ Creating a new task                                  │
└───────────────────────────────────────────────────────────┘

 📝 Enter task title: Buy groceries
 📄 Enter task description (optional): Milk and bread

┌───────────────────────────────────────────────────────────┐
│  ✅ Task created with ID: 1                              │
└───────────────────────────────────────────────────────────┘

[Returns to MENU]

 👉 Enter your choice: 2

[VIEW TASKS screen]

┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃  ID  ┃       Title        ┃   Description   ┃  Status   ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│  1   │  Buy groceries     │  Milk and bread │ ⏳ Pending│
└──────┴────────────────────┴─────────────────┴───────────┘

                     📊 Total: 1 task(s)

[Returns to MENU]

 👉 Enter your choice: 5

[MARK COMPLETE screen]

┌───────────────── MARK TASK COMPLETE ─────────────────────┐
│  ✅ Mark task as completed                              │
└───────────────────────────────────────────────────────────┘

 🔢 Enter task ID: 1

┌───────────────────────────────────────────────────────────┐
│  ✅ Task 1 marked as complete!                           │
└───────────────────────────────────────────────────────────┘

[Returns to MENU]

 👉 Enter your choice: 7

[EXIT screen]

┌───────────────────────────────────────────────────────────┐
│  👋 Thank you for using Todo App!                        │
│  Stay organized and productive!                          │
└───────────────────────────────────────────────────────────┘

[Application exits]
```

## Color Palette Summary

- **Cyan** (#00FFFF): Borders, prompts, links, info
- **Magenta** (#FF00FF): Titles, headers, emphasis
- **Green** (#00FF00): Success, completed
- **Yellow** (#FFFF00): Warnings, pending, taglines
- **Red** (#FF0000): Errors, critical actions
- **White** (Bold): Primary content, menu options

## Typography Hierarchy

1. **Large ASCII Art**: Bold Magenta - Application title
2. **Panel Titles**: Bold Magenta - Section headers
3. **Menu Options**: Bold White - Interactive choices
4. **Prompts**: Bold Cyan - User input requests
5. **Success Messages**: Bold Green - Positive feedback
6. **Error Messages**: Bold Red - Negative feedback
7. **Status Indicators**: Bold Green/Yellow - Task states
8. **Body Text**: White - General content

## Layout Principles

- Consistent padding (0-2 units) in panels
- Clear visual hierarchy through size and color
- Generous use of whitespace
- Aligned columns in tables
- Centered statistics and totals
- Consistent border styles (rounded for panels, box-drawing for tables)

## Accessibility Features

- Emojis supplement color for status
- Text labels for all operations
- Clear error messages with specific guidance
- Consistent structure aids navigation
- High contrast color combinations

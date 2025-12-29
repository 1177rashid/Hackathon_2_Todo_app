# Quickstart: Phase I In-Memory CLI Todo Application

**Branch**: `001-phase1-inmemory-cli`
**Date**: 2025-12-29

---

## Prerequisites

- Python 3.x installed (any modern version)
- Terminal/console access

---

## Running the Application

From the repository root:

```bash
python src/main.py
```

---

## Using the Application

### Main Menu

When the application starts, you will see a numbered menu:

```
=== Todo Application ===

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

Enter your choice:
```

Enter the number of your choice and press Enter.

---

## Operations

### 1. Add Task

Creates a new task with an auto-generated ID.

**Prompts**:
- Enter task title (required)
- Enter task description (optional, press Enter to skip)

**Example**:
```
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread

Task created with ID: 1
```

---

### 2. View Tasks

Displays all tasks with their ID, title, description, and completion status.

**Example (with tasks)**:
```
=== Task List ===

[1] Buy groceries
    Description: Milk, eggs, bread
    Status: Incomplete

[2] Call dentist
    Description:
    Status: Complete

Total: 2 tasks
```

**Example (empty)**:
```
No tasks found. Add a task to get started!
```

---

### 3. Update Task

Modifies an existing task's title and/or description.

**Prompts**:
- Enter task ID
- Enter new title (or press Enter to keep current)
- Enter new description (or press Enter to keep current)

**Example**:
```
Enter task ID: 1
Current title: Buy groceries
Enter new title (or press Enter to keep): Buy groceries and supplies
Current description: Milk, eggs, bread
Enter new description (or press Enter to keep): Milk, eggs, bread, paper towels

Task 1 updated successfully.
```

---

### 4. Delete Task

Permanently removes a task.

**Prompts**:
- Enter task ID

**Example**:
```
Enter task ID: 2

Task 2 deleted successfully.
```

---

### 5. Mark Task Complete

Sets a task's status to complete.

**Prompts**:
- Enter task ID

**Example**:
```
Enter task ID: 1

Task 1 marked as complete.
```

---

### 6. Mark Task Incomplete

Sets a task's status to incomplete.

**Prompts**:
- Enter task ID

**Example**:
```
Enter task ID: 1

Task 1 marked as incomplete.
```

---

### 7. Exit

Exits the application.

```
Goodbye!
```

**Note**: All tasks are lost when you exit (Phase I is in-memory only).

---

## Error Handling

The application handles errors gracefully:

**Invalid menu choice**:
```
Enter your choice: abc
Invalid choice. Please enter a number between 1 and 7.
```

**Task not found**:
```
Enter task ID: 99
Error: Task with ID 99 not found.
```

**Empty title**:
```
Enter task title:
Error: Title cannot be empty.
```

**Invalid task ID format**:
```
Enter task ID: abc
Error: Please enter a valid task ID (number).
```

---

## Important Notes

1. **No Persistence**: All data is lost when you exit the application
2. **Single User**: Designed for one user at a time
3. **Sequential IDs**: Task IDs start at 1 and increment; deleted IDs are not reused
4. **Deterministic Order**: Tasks always appear in the order they were created

---

## Verification Checklist

After running the application, verify:

- [ ] Application starts and displays menu
- [ ] Can add a task with title only
- [ ] Can add a task with title and description
- [ ] Can view tasks (shows all fields)
- [ ] Can update a task's title
- [ ] Can update a task's description
- [ ] Can delete a task
- [ ] Can mark a task complete
- [ ] Can mark a task incomplete
- [ ] Invalid inputs show helpful error messages (no crashes)
- [ ] Exit terminates cleanly

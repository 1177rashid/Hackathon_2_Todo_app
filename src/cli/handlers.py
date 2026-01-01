"""
Operation Handlers - CLI Presentation Layer

Handlers for all task operations per User Stories 1-6.
Extended with Task Sorting support (FR-020 through FR-024).
Extended with tag operations per FR-006 through FR-011.
"""

import sys
import os
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.state.task_store import TaskStore
from src.utils.task_sorter import sort_tasks, SortBy, get_valid_sort_options
from src.cli.display import (
    display_success, display_error, display_task_list,
    read_task_id, read_text, validate_title, read_priority,
    display_operation_header, display_current_values, display_no_search_results,
    read_date_input, read_recurrence_input
)


def handle_add_task(store: TaskStore):
    """
    Handle add task operation (FR-007 to FR-010, User Story 2).
    Extended with priority support per FR-001, FR-002 (Task Organization).
    Extended with due date and recurrence support for advanced features.

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("ADD NEW TASK", "➕")

        # Prompt for title (required)
        title = read_text("Enter task title", required=True, emoji="📝")
        if title is None:  # Validation failed
            return

        # Validate title is not empty/whitespace-only (FR-009)
        if not validate_title(title):
            display_error("Title cannot be empty or whitespace-only.")
            return

        # Prompt for description (optional)
        description = read_text("Enter task description (optional)", required=False, emoji="📄")

        # Prompt for priority (optional, defaults to medium per FR-002)
        priority = read_priority("Enter priority (press Enter for default 'medium')")

        # Prompt for due date (optional)
        due_date = read_date_input("Enter due date")

        # Prompt for recurrence pattern (optional)
        recurrence_pattern = read_recurrence_input("Enter recurrence pattern")

        # If recurrence is set but no due date, warn user
        if recurrence_pattern and not due_date:
            display_error("Recurring tasks must have a due date. Please set a due date.")
            return

        # Create task with all parameters (FR-007, FR-008)
        task = store.add_task(
            title,
            description,
            priority=priority,
            due_date=due_date,
            recurrence_pattern=recurrence_pattern
        )

        # Display success with ID (FR-010)
        display_success(f"Task created with ID: {task.id}")

    except ValueError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to add task: {str(e)}")


def handle_view_tasks(store: TaskStore):
    """
    Handle view tasks operation (FR-011 to FR-014, User Story 1).
    Extended with Task Sorting support (FR-020 through FR-024).

    Args:
        store: TaskStore instance
    """
    try:
        # Get all tasks (FR-011)
        tasks = store.get_all_tasks()

        # Prompt for sort option (FR-020, FR-021, FR-022)
        sort_by = _read_sort_option()

        # Sort tasks if option selected (FR-024 - sorting only affects display)
        if sort_by is not None:
            tasks = sort_tasks(tasks, sort_by)

        # Display tasks or empty message (FR-012, FR-013, FR-014)
        display_task_list(tasks, sort_by=sort_by)

    except Exception as e:
        display_error(f"Failed to view tasks: {str(e)}")


def _read_sort_option() -> Optional[str]:
    """
    Read and validate sort option for task list (FR-020 through FR-024).

    Returns:
        Sort option string (title/priority/due-date) or None for no sorting
    """
    from rich.prompt import Prompt

    # Build sort options display
    options = [
        "1. No sorting (creation order)",
        "2. Sort by title (A-Z)",
        "3. Sort by priority (High → Medium → Low)",
        "4. Sort by due date (oldest first)"
    ]

    # Display sort options
    display_operation_header("SORT OPTIONS", "🔀")
    for option in options:
        from rich.console import Console
        console = Console()
        console.print(f"  [bold white]{option}[/bold white]")

    # Read user choice
    try:
        choice = Prompt.ask("\n[bold cyan]👉 Enter sort option (1-4, press Enter for no sorting)[/bold cyan]", default="")

        if not choice or choice.strip() == "":
            return None

        choice_int = int(choice)

        # Map choice to sort option
        if choice_int == 1:
            return None
        elif choice_int == 2:
            return SortBy.TITLE
        elif choice_int == 3:
            return SortBy.PRIORITY
        elif choice_int == 4:
            return SortBy.DUE_DATE
        else:
            display_error("Please enter a number between 1 and 4.")
            return None

    except ValueError:
        display_error("Please enter a valid number.")
        return None


def handle_update_task(store: TaskStore):
    """
    Handle update task operation (FR-015 to FR-019, User Story 4).
    Extended with priority update support per FR-005 (Task Organization).

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("UPDATE TASK", "✏️")

        # Prompt for task ID
        task_id = read_task_id("Enter task ID")
        if task_id is None:
            return

        # Check if task exists
        task = store.get_task(task_id)
        if not task:
            display_error(f"Task with ID {task_id} not found.")  # FR-019
            return

        # Show current values
        display_current_values(task)

        # Prompt for new title (press Enter to keep)
        new_title = read_text("Enter new title (or press Enter to keep current)", required=False, emoji="📝")
        if new_title == "":
            new_title = None  # Keep current

        # Validate new title if provided (FR-017)
        if new_title is not None and not validate_title(new_title):
            display_error("Title cannot be empty or whitespace-only.")
            return

        # Prompt for new description (press Enter to keep)
        new_description = read_text("Enter new description (or press Enter to keep current)", required=False, emoji="📄")
        if new_description == "":
            new_description = None  # Keep current

        # Prompt for new priority (press Enter to keep, FR-005)
        new_priority = read_priority("Enter new priority (press Enter to keep current)")

        # Update task (FR-015, FR-016, FR-018, FR-005)
        store.update_task(
            task_id,
            title=new_title,
            description=new_description,
            priority=new_priority
        )

        display_success(f"Task {task_id} updated successfully!")

    except ValueError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to update task: {str(e)}")


def handle_delete_task(store: TaskStore):
    """
    Handle delete task operation (FR-020 to FR-022, User Story 5).

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("DELETE TASK", "❌")

        # Prompt for task ID
        task_id = read_task_id("Enter task ID")
        if task_id is None:
            return

        # Delete task (FR-020)
        success = store.delete_task(task_id)

        if success:
            display_success(f"Task {task_id} deleted successfully!")  # FR-021
        else:
            display_error(f"Task with ID {task_id} not found.")  # FR-022

    except Exception as e:
        display_error(f"Failed to delete task: {str(e)}")


def handle_mark_complete(store: TaskStore):
    """
    Handle mark complete operation (FR-023, FR-025, User Story 3).

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("MARK TASK COMPLETE", "✅")

        # Prompt for task ID
        task_id = read_task_id("Enter task ID")
        if task_id is None:
            return

        # Mark task complete (FR-023)
        success = store.mark_complete(task_id)

        if success:
            display_success(f"Task {task_id} marked as complete!")
        else:
            display_error(f"Task with ID {task_id} not found.")  # FR-025

    except Exception as e:
        display_error(f"Failed to mark task complete: {str(e)}")


def handle_mark_incomplete(store: TaskStore):
    """
    Handle mark incomplete operation (FR-024, FR-025, User Story 3).

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("MARK TASK INCOMPLETE", "🔄")

        # Prompt for task ID
        task_id = read_task_id("Enter task ID")
        if task_id is None:
            return

        # Mark task incomplete (FR-024)
        success = store.mark_incomplete(task_id)

        if success:
            display_success(f"Task {task_id} marked as incomplete!")
        else:
            display_error(f"Task with ID {task_id} not found.")  # FR-025

    except Exception as e:
        display_error(f"Failed to mark task incomplete: {str(e)}")


def handle_search_tasks(store: TaskStore):
    """
    Handle search tasks operation (FR-012, FR-013, FR-014).

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("SEARCH TASKS", "🔍")

        # Prompt for search keyword
        keyword = read_text("Enter search keyword", required=True, emoji="🔑")
        if keyword is None:  # Validation failed
            return

        # Validate keyword is not empty/whitespace-only
        if not keyword or not keyword.strip():
            display_error("Search keyword cannot be empty or whitespace-only.")
            return

        # Search tasks (FR-012, FR-013)
        matching_tasks = store.search_tasks(keyword)

        # Display results (FR-014)
        if not matching_tasks:
            display_no_search_results(keyword.strip())
        else:
            display_task_list(matching_tasks)

    except Exception as e:
        display_error(f"Failed to search tasks: {str(e)}")


def handle_add_tag(store: TaskStore):
    """
    Handle add tag to task operation (FR-008).

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("ADD TAG TO TASK", "🏷️")

        # Prompt for task ID
        task_id = read_task_id("Enter task ID")
        if task_id is None:
            return

        # Check if task exists
        task = store.get_task(task_id)
        if not task:
            display_error(f"Task with ID {task_id} not found.")
            return

        # Show current tags
        current_tags = ", ".join(task.tags) if task.tags else "(no tags)"
        from rich.console import Console
        console = Console()
        console.print(f"\n[cyan]Current tags:[/cyan] {current_tags}")

        # Prompt for tag to add
        tag = read_text("Enter tag to add", required=True, emoji="🏷️")
        if tag is None:  # Validation failed
            return

        # Validate tag is not empty/whitespace-only
        if not tag or not tag.strip():
            display_error("Tag cannot be empty or whitespace-only.")
            return

        # Add tag (FR-008)
        success = store.add_tag(task_id, tag.strip())

        if success:
            display_success(f"Tag '{tag.strip()}' added to task {task_id}!")
        else:
            # Tag already exists (FR-007)
            display_error(f"Tag '{tag.strip()}' already exists on this task.")

    except ValueError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to add tag: {str(e)}")


def handle_remove_tag(store: TaskStore):
    """
    Handle remove tag from task operation (FR-009).

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("REMOVE TAG FROM TASK", "🏷️")

        # Prompt for task ID
        task_id = read_task_id("Enter task ID")
        if task_id is None:
            return

        # Check if task exists
        task = store.get_task(task_id)
        if not task:
            display_error(f"Task with ID {task_id} not found.")
            return

        # Show current tags
        if not task.tags:
            display_error("This task has no tags to remove.")
            return

        current_tags = ", ".join(task.tags)
        from rich.console import Console
        console = Console()
        console.print(f"\n[cyan]Current tags:[/cyan] {current_tags}")

        # Prompt for tag to remove
        tag = read_text("Enter tag to remove", required=True, emoji="🏷️")
        if tag is None:  # Validation failed
            return

        # Remove tag (FR-009)
        success = store.remove_tag(task_id, tag.strip())

        if success:
            display_success(f"Tag '{tag.strip()}' removed from task {task_id}!")
        else:
            # Tag not present
            display_error(f"Tag '{tag.strip()}' not found on this task.")

    except ValueError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to remove tag: {str(e)}")


def handle_replace_tags(store: TaskStore):
    """
    Handle replace all tags on task operation (FR-010).

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("REPLACE ALL TAGS", "🏷️")

        # Prompt for task ID
        task_id = read_task_id("Enter task ID")
        if task_id is None:
            return

        # Check if task exists
        task = store.get_task(task_id)
        if not task:
            display_error(f"Task with ID {task_id} not found.")
            return

        # Show current tags
        current_tags = ", ".join(task.tags) if task.tags else "(no tags)"
        from rich.console import Console
        console = Console()
        console.print(f"\n[cyan]Current tags:[/cyan] {current_tags}")

        # Prompt for new tags (comma-separated)
        tags_input = read_text("Enter new tags (comma-separated, or press Enter to clear all tags)", required=False, emoji="🏷️")

        # Handle empty input (clear all tags)
        if tags_input == "":
            tags_list = []
        else:
            # Parse comma-separated tags
            tags_list = [t.strip() for t in tags_input.split(",")]
            # Remove empty strings
            tags_list = [t for t in tags_list if t]

        # Replace tags (FR-010)
        store.replace_tags(task_id, tags_list)

        if tags_list:
            display_success(f"Tags for task {task_id} replaced with: {', '.join(tags_list)}")
        else:
            display_success(f"All tags removed from task {task_id}")

    except ValueError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to replace tags: {str(e)}")


def handle_view_overdue_tasks(store: TaskStore):
    """
    Handle view overdue tasks operation.

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("VIEW OVERDUE TASKS", "⚠️")

        # Get overdue tasks
        overdue_tasks = store.get_overdue_tasks()

        # Display tasks or empty message
        if not overdue_tasks:
            display_no_overdue_tasks()
        else:
            display_task_list(overdue_tasks)

    except Exception as e:
        display_error(f"Failed to view overdue tasks: {str(e)}")


def handle_view_by_due_date(store: TaskStore):
    """
    Handle view tasks sorted by due date operation.

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("VIEW TASKS BY DUE DATE", "📅")

        # Get tasks sorted by due date
        tasks = store.get_sorted_by_due_date()

        # Display tasks or empty message
        display_task_list(tasks, sort_by="due-date")

    except Exception as e:
        display_error(f"Failed to view tasks by due date: {str(e)}")


def handle_set_recurrence(store: TaskStore):
    """
    Handle set recurrence pattern on task operation.

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("SET RECURRENCE", "🔄")

        # Prompt for task ID
        task_id = read_task_id("Enter task ID")
        if task_id is None:
            return

        # Check if task exists
        task = store.get_task(task_id)
        if not task:
            display_error(f"Task with ID {task_id} not found.")
            return

        # Show current recurrence
        current_rec = task.recurrence_pattern.get('type', 'none') if task.recurrence_pattern else 'none'
        current_rec = current_rec.capitalize()
        from rich.console import Console
        console = Console()
        console.print(f"\n[cyan]Current recurrence:[/cyan] {current_rec}")

        # Prompt for new recurrence pattern
        new_recurrence = read_recurrence_input("Enter new recurrence pattern")

        # If recurrence is set but task has no due date, warn user
        if new_recurrence and not task.due_date:
            display_error("Recurring tasks must have a due date. Please set a due date first.")
            return

        # Update task directly (update_task doesn't support recurrence yet)
        task.recurrence_pattern = new_recurrence

        if new_recurrence:
            rec_type = new_recurrence.get('type', '').capitalize()
            display_success(f"Task {task_id} is now recurring ({rec_type})")
        else:
            display_success(f"Task {task_id} is no longer recurring")

    except ValueError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to set recurrence: {str(e)}")


def handle_complete_with_recurrence(store: TaskStore):
    """
    Handle complete task operation with recurrence support.
    For recurring tasks, generates next instance automatically.

    Args:
        store: TaskStore instance
    """
    try:
        # Display operation header
        display_operation_header("COMPLETE TASK", "✅")

        # Prompt for task ID
        task_id = read_task_id("Enter task ID")
        if task_id is None:
            return

        # Check if task exists
        task = store.get_task(task_id)
        if not task:
            display_error(f"Task with ID {task_id} not found.")
            return

        # Check if task is recurring
        if task.recurrence_pattern:
            # Use complete_task to handle recurrence
            new_task = store.complete_task(task_id)

            if new_task:
                display_success(
                    f"Task {task_id} completed! "
                    f"Next instance created with ID: {new_task.id}"
                )
            else:
                display_error(f"Task with ID {task_id} not found.")
        else:
            # Use mark_complete for non-recurring tasks
            success = store.mark_complete(task_id)

            if success:
                display_success(f"Task {task_id} marked as complete!")
            else:
                display_error(f"Task with ID {task_id} not found.")

    except ValueError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to complete task: {str(e)}")

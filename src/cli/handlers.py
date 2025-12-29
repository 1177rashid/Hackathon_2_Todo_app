"""
Operation Handlers - CLI Presentation Layer

Handlers for all task operations per User Stories 1-6.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.state.task_store import TaskStore
from src.cli.display import (
    display_success, display_error, display_task_list,
    read_task_id, read_text, validate_title,
    display_operation_header, display_current_values
)


def handle_add_task(store: TaskStore):
    """
    Handle add task operation (FR-007 to FR-010, User Story 2).

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

        # Create task (FR-007, FR-008)
        task = store.add_task(title, description)

        # Display success with ID (FR-010)
        display_success(f"Task created with ID: {task.id}")

    except Exception as e:
        display_error(f"Failed to add task: {str(e)}")


def handle_view_tasks(store: TaskStore):
    """
    Handle view tasks operation (FR-011 to FR-014, User Story 1).

    Args:
        store: TaskStore instance
    """
    try:
        # Get all tasks (FR-011)
        tasks = store.get_all_tasks()

        # Display tasks or empty message (FR-012, FR-013, FR-014)
        display_task_list(tasks)

    except Exception as e:
        display_error(f"Failed to view tasks: {str(e)}")


def handle_update_task(store: TaskStore):
    """
    Handle update task operation (FR-015 to FR-019, User Story 4).

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

        # Update task (FR-015, FR-016, FR-018)
        store.update_task(task_id, title=new_title, description=new_description)

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

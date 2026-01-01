"""
Task Sorter - Utility Module

Provides sorting functionality for tasks per FR-020 through FR-024.
Supports sorting by title, priority, and due date.
"""

from typing import List, Optional
import sys
import os

# Add parent directory to path to import domain module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.domain.task import Task, TaskPriority


class SortBy:
    """Sort options for task display."""
    TITLE = "title"
    PRIORITY = "priority"
    DUE_DATE = "due-date"
    NONE = None


def sort_tasks(tasks: List[Task], sort_by: Optional[str] = None) -> List[Task]:
    """
    Sort tasks by specified criteria (FR-020, FR-021, FR-022, FR-023).

    Sorting only affects display order; original task data remains unchanged (FR-024).
    Returns a new sorted list, does not modify the input list.

    Args:
        tasks: List of tasks to sort
        sort_by: Sort criteria - "title", "priority", "due-date", or None

    Returns:
        Sorted copy of the task list (new list, input unchanged)

    Raises:
        ValueError: If sort_by is not a valid sort option
    """
    # Create a copy to avoid modifying original (FR-024)
    sorted_tasks = tasks.copy()

    if sort_by is None:
        # Return tasks in original order (creation order)
        return sorted_tasks

    if sort_by == SortBy.TITLE:
        return _sort_by_title(sorted_tasks)
    elif sort_by == SortBy.PRIORITY:
        return _sort_by_priority(sorted_tasks)
    elif sort_by == SortBy.DUE_DATE:
        return _sort_by_due_date(sorted_tasks)
    else:
        raise ValueError(
            f"Invalid sort option '{sort_by}'. "
            f"Valid options are: {SortBy.TITLE}, {SortBy.PRIORITY}, {SortBy.DUE_DATE}"
        )


def _sort_by_title(tasks: List[Task]) -> List[Task]:
    """
    Sort tasks alphabetically by title (case-insensitive) (FR-020).

    Args:
        tasks: List of tasks to sort

    Returns:
        Tasks sorted by title (case-insensitive)
    """
    # Stable sort by title (case-insensitive) using lower() for comparison
    # Use key to ensure case-insensitive sorting while preserving original strings
    return sorted(tasks, key=lambda task: task.title.lower())


def _sort_by_priority(tasks: List[Task]) -> List[Task]:
    """
    Sort tasks by priority (HIGH > MEDIUM > LOW) (FR-021).

    Args:
        tasks: List of tasks to sort

    Returns:
        Tasks sorted by priority (HIGH first, then MEDIUM, then LOW)
    """
    # Priority order mapping for sorting
    priority_order = {
        TaskPriority.HIGH: 0,
        TaskPriority.MEDIUM: 1,
        TaskPriority.LOW: 2
    }

    # Stable sort by priority
    return sorted(tasks, key=lambda task: priority_order[task.priority])


def _sort_by_due_date(tasks: List[Task]) -> List[Task]:
    """
    Sort tasks by due date (chronological) (FR-022).
    Tasks without due dates appear last (FR-023).

    Args:
        tasks: List of tasks to sort

    Returns:
        Tasks sorted by due date (oldest first), tasks without due dates last
    """
    def due_date_key(task: Task):
        """
        Key function for sorting by due date.
        Returns a tuple: (has_date, date_value)
        Tasks with dates get (True, date), without dates get (False, None).
        This ensures tasks without dates always appear last, while dated tasks sort chronologically.
        """
        if task.due_date is None:
            # Use tuple (False, None) so tasks without dates sort last
            return (False, None)
        return (True, task.due_date)

    # Stable sort by due date
    return sorted(tasks, key=due_date_key)


def get_valid_sort_options() -> List[str]:
    """
    Get list of valid sort options for display purposes.

    Returns:
        List of valid sort option strings
    """
    return [SortBy.TITLE, SortBy.PRIORITY, SortBy.DUE_DATE]

"""
Task Store - State Management Layer

In-memory task storage maintaining creation order per FR-005, FR-006, FR-014.
"""

from typing import List, Optional
import sys
import os

# Add parent directory to path to import domain module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain.task import Task


class TaskStore:
    """
    In-memory task collection with sequential ID generation.

    Maintains deterministic ordering (creation order) and ensures ID stability.
    """

    def __init__(self):
        """Initialize empty task store with ID counter starting at 1."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create and add a new task.

        Args:
            title: Task title (required, non-empty)
            description: Optional task description

        Returns:
            The created Task with assigned ID

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        # Create task with auto-generated ID (FR-001)
        task = Task(self._next_id, title, description)

        # Add to collection (maintains insertion order)
        self._tasks.append(task)

        # Increment ID counter (never reuse deleted IDs per FR-005)
        self._next_id += 1

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in creation order (FR-014).

        Returns:
            List of all tasks (may be empty)
        """
        return self._tasks.copy()

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> bool:
        """
        Update task title and/or description.

        Args:
            task_id: Task identifier
            title: New title (None to keep current, empty string rejected)
            description: New description (None to keep current, empty string allowed)

        Returns:
            True if task updated, False if not found

        Raises:
            ValueError: If new title is empty or whitespace-only
        """
        task = self.get_task(task_id)
        if not task:
            return False

        # Update title if provided (FR-015, FR-017)
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty or whitespace-only")
            task.title = title.strip()

        # Update description if provided (FR-016, FR-018)
        if description is not None:
            task.description = description

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete task by ID.

        Args:
            task_id: Task identifier

        Returns:
            True if task deleted, False if not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        self._tasks.remove(task)
        return True

    def mark_complete(self, task_id: int) -> bool:
        """
        Mark task as complete (FR-023).

        Args:
            task_id: Task identifier

        Returns:
            True if task marked complete, False if not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        task.completed = True
        return True

    def mark_incomplete(self, task_id: int) -> bool:
        """
        Mark task as incomplete (FR-024).

        Args:
            task_id: Task identifier

        Returns:
            True if task marked incomplete, False if not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        task.completed = False
        return True

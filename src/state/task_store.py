"""
Task Store - State Management Layer

In-memory task storage maintaining creation order per FR-005, FR-006, FR-014.
Extended with due_date support for Task Sorting (FR-020 through FR-024).
Extended with tag operations per FR-006 through FR-011.
Extended with recurrence support for Advanced Todo features.
"""

from typing import List, Optional, Union, Dict, Any
from datetime import date, datetime
import sys
import os

# Add parent directory to path to import domain module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain.task import Task, TaskPriority
from state.recurrence_policy import validate_recurrence_pattern, calculate_next_due_date


class TaskStore:
    """
    In-memory task collection with sequential ID generation.

    Maintains deterministic ordering (creation order) and ensures ID stability.
    """

    def __init__(self):
        """Initialize empty task store with ID counter starting at 1."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: Optional[Union[str, TaskPriority]] = None,
        due_date: Optional[date] = None,
        tags: Optional[List[str]] = None,
        recurrence_pattern: Optional[Dict[str, Any]] = None
    ) -> Task:
        """
        Create and add a new task.

        Args:
            title: Task title (required, non-empty)
            description: Optional task description
            priority: Task priority (string or TaskPriority, defaults to MEDIUM per FR-002)
            due_date: Optional due date (defaults to None per FR-022)
            tags: Optional list of tag strings (defaults to empty list per FR-006)
            recurrence_pattern: Optional recurrence pattern dict (defaults to None for non-recurring tasks)

        Returns:
            The created Task with assigned ID

        Raises:
            ValueError: If title is empty or whitespace-only, priority is invalid,
                        or recurrence_pattern is invalid
        """
        # Convert string priority to enum if needed (FR-001, FR-003)
        if priority is None:
            task_priority = TaskPriority.MEDIUM
        elif isinstance(priority, str):
            task_priority = TaskPriority.from_string(priority)
        else:
            task_priority = priority

        # Validate recurrence pattern if provided
        if recurrence_pattern is not None:
            if not validate_recurrence_pattern(recurrence_pattern):
                raise ValueError(
                    f"Invalid recurrence pattern: {recurrence_pattern}. "
                    "Allowed patterns: None, {'type': 'daily'}, {'type': 'weekly'}, {'type': 'monthly'}"
                )

        # Create task with auto-generated ID (FR-001)
        task = Task(
            self._next_id,
            title,
            description,
            priority=task_priority,
            due_date=due_date,
            tags=tags,
            recurrence_pattern=recurrence_pattern
        )

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

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Union[str, TaskPriority]] = None
    ) -> bool:
        """
        Update task title, description, and/or priority.

        Args:
            task_id: Task identifier
            title: New title (None to keep current, empty string rejected)
            description: New description (None to keep current, empty string allowed)
            priority: New priority (None to keep current, FR-005)

        Returns:
            True if task updated, False if not found

        Raises:
            ValueError: If new title is empty or whitespace-only, or priority is invalid
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

        # Update priority if provided (FR-005)
        if priority is not None:
            if isinstance(priority, str):
                task_priority = TaskPriority.from_string(priority)
            else:
                task_priority = priority
            task.priority = task_priority

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

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title or description (FR-012, FR-013).

        Performs case-insensitive search across task title and description fields.
        Returns tasks that contain keyword in either field.

        Args:
            keyword: Search keyword to match against title/description

        Returns:
            List of matching tasks (may be empty). Maintains original creation order.
        """
        if not keyword or not keyword.strip():
            return []

        keyword_lower = keyword.strip().lower()
        matching_tasks = []

        for task in self._tasks:
            # Search in title (case-insensitive)
            title_match = keyword_lower in task.title.lower()

            # Search in description (case-insensitive, handle empty description)
            description = task.description or ""
            description_match = keyword_lower in description.lower()

            # Include task if keyword matches title OR description
            if title_match or description_match:
                matching_tasks.append(task)

        return matching_tasks

    def add_tag(self, task_id: int, tag: str) -> bool:
        """
        Add a tag to an existing task (FR-008).

        Prevents duplicate tags on the same task (FR-007).
        Rejects empty or whitespace-only tags.

        Args:
            task_id: Task identifier
            tag: Tag to add

        Returns:
            True if tag added, False if task not found

        Raises:
            ValueError: If tag is empty or whitespace-only
        """
        # Validate tag is not empty
        if not tag or not tag.strip():
            raise ValueError("Tags cannot be empty or whitespace-only")

        tag_stripped = tag.strip()

        task = self.get_task(task_id)
        if not task:
            return False

        # Prevent duplicate tags (FR-007)
        if tag_stripped in task.tags:
            return False  # Tag already exists, no-op

        # Add tag (FR-008)
        task.tags.append(tag_stripped)
        return True

    def remove_tag(self, task_id: int, tag: str) -> bool:
        """
        Remove a specific tag from a task (FR-009).

        Args:
            task_id: Task identifier
            tag: Tag to remove

        Returns:
            True if tag removed, False if task not found or tag not present
        """
        tag_stripped = tag.strip()

        task = self.get_task(task_id)
        if not task:
            return False

        # Remove tag if present (FR-009)
        if tag_stripped in task.tags:
            task.tags.remove(tag_stripped)
            return True

        return False

    def replace_tags(self, task_id: int, tags: List[str]) -> bool:
        """
        Replace all tags on a task with a new set (FR-010).

        Rejects empty strings in tags and prevents duplicates.

        Args:
            task_id: Task identifier
            tags: New list of tags to replace current tags

        Returns:
            True if tags replaced, False if task not found

        Raises:
            ValueError: If any tag is empty or whitespace-only
        """
        # Validate all tags (FR-007)
        validated_tags = []
        for tag in tags:
            tag_stripped = tag.strip()
            if not tag_stripped:
                raise ValueError("Tags cannot be empty or whitespace-only")
            # Prevent duplicates (FR-007)
            if tag_stripped not in validated_tags:
                validated_tags.append(tag_stripped)

        task = self.get_task(task_id)
        if not task:
            return False

        # Replace all tags (FR-010)
        task.tags = validated_tags
        return True

    def complete_task(self, task_id: int) -> Optional[Task]:
        """
        Mark task as complete and generate next instance if recurring.

        For non-recurring tasks, this behaves identically to mark_complete().
        For recurring tasks, marks the task complete and creates a new instance
        with the next due date calculated from the recurrence pattern.

        Args:
            task_id: Task identifier

        Returns:
            The new task instance created (for recurring tasks), None if no new task created

        Raises:
            ValueError: If task is recurring but has no due date
        """
        task = self.get_task(task_id)
        if not task:
            return None

        # Mark current task as complete
        task.completed = True

        # Handle recurrence if task has a recurrence pattern
        if task.recurrence_pattern is not None:
            # Recurring tasks must have a due date to calculate next occurrence
            if task.due_date is None:
                raise ValueError(
                    f"Recurring task {task_id} must have a due date to generate next instance"
                )

            # Calculate next due date
            next_due_date = calculate_next_due_date(task.due_date, task.recurrence_pattern)

            # Create new task instance with copied properties
            new_task = self.add_task(
                title=task.title,
                description=task.description,
                priority=task.priority,
                due_date=next_due_date,
                tags=task.tags.copy() if task.tags else None,
                recurrence_pattern=task.recurrence_pattern.copy()
            )

            return new_task

        return None

    def get_sorted_by_due_date(self) -> List[Task]:
        """
        Retrieve all tasks sorted by due date (earliest first).

        Tasks without due dates appear at the end.
        Maintains relative order among tasks with the same due date.

        Returns:
            List of tasks sorted by due date (ascending)
        """
        # Separate tasks with and without due dates
        tasks_with_due = [t for t in self._tasks if t.due_date is not None]
        tasks_without_due = [t for t in self._tasks if t.due_date is None]

        # Sort tasks with due dates
        tasks_with_due.sort(key=lambda t: t.due_date)

        # Combine: tasks with due dates first, then tasks without
        return tasks_with_due + tasks_without_due

    def get_overdue_tasks(self) -> List[Task]:
        """
        Retrieve all overdue tasks (incomplete tasks with due_date in the past).

        A task is overdue if:
        - It is not completed
        - It has a due date
        - The due date is before today

        Returns:
            List of overdue tasks in creation order
        """
        today = date.today()

        overdue_tasks = [
            task for task in self._tasks
            if not task.completed
            and task.due_date is not None
            and task.due_date < today
        ]

        return overdue_tasks

"""
Task Entity - Domain Layer

Represents a unit of work to be tracked. Enforces domain invariants per FR-001 through FR-005.
Extended with priority support per FR-001 through FR-005 (Task Organization).
Extended with due_date support for Task Sorting (FR-020 through FR-024).
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import date


class TaskPriority(Enum):
    """
    Task priority levels.

    Values:
        - HIGH: Urgent tasks requiring immediate attention
        - MEDIUM: Standard priority tasks (default)
        - LOW: Low priority tasks to be addressed when time permits
    """
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @classmethod
    def from_string(cls, value: str) -> 'TaskPriority':
        """
        Convert a string to TaskPriority.

        Args:
            value: String representation of priority (case-insensitive)

        Returns:
            Corresponding TaskPriority enum value

        Raises:
            ValueError: If string does not match any valid priority
        """
        valid_priorities = [p.value for p in cls]
        normalized = value.lower().strip()

        for priority in cls:
            if priority.value == normalized:
                return priority

        raise ValueError(
            f"Invalid priority '{value}'. Valid options are: {', '.join(valid_priorities)}"
        )


class Task:
    """
    Task entity with attributes: id, title, description, completed, priority, due_date, tags, recurrence_pattern.

    Invariants:
    - ID is a positive integer, immutable after creation
    - Title is required, non-empty after stripping whitespace
    - Description is optional (may be empty)
    - Completed defaults to False
    - Priority defaults to MEDIUM (FR-002)
    - Due date is optional (FR-022)
    - Tags is a list of non-empty, unique string labels (FR-006, FR-007)
    - Recurrence pattern is optional dict with 'type' key ('daily', 'weekly', 'monthly', or None)
    """

    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        completed: bool = False,
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date: Optional[date] = None,
        tags: List[str] = None,
        recurrence_pattern: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a Task.

        Args:
            task_id: Unique positive integer identifier
            title: Task title (required, non-empty after strip)
            description: Optional task description
            completed: Completion status (defaults to False)
            priority: Task priority (defaults to MEDIUM per FR-002)
            due_date: Optional due date (defaults to None per FR-022)
            tags: Optional list of tag strings (defaults to empty list per FR-006)
            recurrence_pattern: Optional recurrence pattern dict (defaults to None for non-recurring tasks)

        Raises:
            ValueError: If title is empty or whitespace-only, or if tags contain empty strings
        """
        # Validate title (FR-002, FR-009, FR-017)
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")

        # Validate tags (FR-007) - prevent empty strings and duplicates
        validated_tags: List[str] = []
        if tags:
            for tag in tags:
                tag_stripped = tag.strip()
                if not tag_stripped:
                    raise ValueError("Tags cannot be empty or whitespace-only")
                # Prevent duplicates (FR-007)
                if tag_stripped not in validated_tags:
                    validated_tags.append(tag_stripped)

        # Set immutable ID (FR-001, FR-005)
        self._id = task_id

        # Set attributes
        self.title = title.strip()
        self.description = description
        self.completed = completed
        self.priority = priority
        self.due_date = due_date
        self.tags = validated_tags
        self.recurrence_pattern = recurrence_pattern

    @property
    def id(self) -> int:
        """Get task ID (immutable)."""
        return self._id

    def __repr__(self) -> str:
        due_str = self.due_date.isoformat() if self.due_date else "None"
        tags_str = str(self.tags) if self.tags else "[]"
        recurrence_str = str(self.recurrence_pattern) if self.recurrence_pattern else "None"
        return (f"Task(id={self.id}, title='{self.title}', completed={self.completed}, "
                f"priority={self.priority.value}, due_date={due_str}, tags={tags_str}, "
                f"recurrence_pattern={recurrence_str})")

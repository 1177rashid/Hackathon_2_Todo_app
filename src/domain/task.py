"""
Task Entity - Domain Layer

Represents a unit of work to be tracked. Enforces domain invariants per FR-001 through FR-005.
"""


class Task:
    """
    Task entity with attributes: id, title, description, completed.

    Invariants:
    - ID is a positive integer, immutable after creation
    - Title is required, non-empty after stripping whitespace
    - Description is optional (may be empty)
    - Completed defaults to False
    """

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a Task.

        Args:
            task_id: Unique positive integer identifier
            title: Task title (required, non-empty after strip)
            description: Optional task description
            completed: Completion status (defaults to False)

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        # Validate title (FR-002, FR-009, FR-017)
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")

        # Set immutable ID (FR-001, FR-005)
        self._id = task_id

        # Set attributes
        self.title = title.strip()
        self.description = description
        self.completed = completed

    @property
    def id(self) -> int:
        """Get task ID (immutable)."""
        return self._id

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"

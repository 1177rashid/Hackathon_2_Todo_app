"""
State Management Module

Provides in-memory task storage and recurrence policy engine.
"""

from .task_store import TaskStore
from .recurrence_policy import (
    validate_recurrence_pattern,
    calculate_next_due_date
)

__all__ = [
    'TaskStore',
    'validate_recurrence_pattern',
    'calculate_next_due_date'
]

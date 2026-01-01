"""
Recurrence Policy Engine

Handles task recurrence pattern validation and next due date calculation.
Supports daily, weekly, and monthly recurrence patterns.
"""

from typing import Optional, Dict, Any
from datetime import date, timedelta
from calendar import monthrange, month_name


def validate_recurrence_pattern(recurrence_pattern: Optional[Dict[str, Any]]) -> bool:
    """
    Validate recurrence pattern structure.

    Allowed patterns:
    - None: No recurrence (default)
    - {'type': 'daily'}: Repeats daily
    - {'type': 'weekly'}: Repeats every 7 days
    - {'type': 'monthly'}: Repeats monthly with day-of-month adjustment

    Args:
        recurrence_pattern: Recurrence pattern dict to validate

    Returns:
        True if pattern is valid, False otherwise
    """
    if recurrence_pattern is None:
        return True

    if not isinstance(recurrence_pattern, dict):
        return False

    pattern_type = recurrence_pattern.get('type')
    valid_types = ['daily', 'weekly', 'monthly']

    return pattern_type in valid_types


def calculate_next_due_date(
    current_due_date: date,
    recurrence_pattern: Dict[str, Any]
) -> Optional[date]:
    """
    Calculate the next due date based on recurrence pattern.

    Calculation rules:
    - daily: Add 1 day to current due date
    - weekly: Add 7 days to current due date
    - monthly: Add 1 month with edge case handling:
      - Jan 31 -> Feb 28/29 (adjusts to last day of month)
      - Feb 30 rejected (invalid date, handled naturally)

    Args:
        current_due_date: Current task due date
        recurrence_pattern: Recurrence pattern dict with 'type' key

    Returns:
        Next due date, or None if pattern is invalid

    Raises:
        ValueError: If recurrence pattern is invalid
    """
    if not validate_recurrence_pattern(recurrence_pattern):
        raise ValueError(f"Invalid recurrence pattern: {recurrence_pattern}")

    pattern_type = recurrence_pattern.get('type')

    if pattern_type == 'daily':
        return current_due_date + timedelta(days=1)
    elif pattern_type == 'weekly':
        return current_due_date + timedelta(weeks=1)
    elif pattern_type == 'monthly':
        # Handle monthly recurrence with edge cases
        year = current_due_date.year
        month = current_due_date.month + 1

        # Handle year rollover
        if month > 12:
            month = 1
            year += 1

        # Get last day of target month
        last_day = monthrange(year, month)[1]

        # Adjust day if current day exceeds last day (e.g., Jan 31 -> Feb 28/29)
        target_day = min(current_due_date.day, last_day)

        return date(year, month, target_day)

    return None

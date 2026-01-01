"""
Input Validators - Utility Layer

Date/time input validation and parsing for advanced todo features.
Supports due dates and recurrence patterns.
"""

from datetime import datetime, date
from typing import Optional, Dict, Any
import re


def parse_date(date_input: str) -> Optional[date]:
    """
    Parse a date string in various formats.

    Supported formats:
    - YYYY-MM-DD (ISO 8601)
    - YYYY/MM/DD
    - MM-DD-YYYY
    - MM/DD/YYYY
    - DD-MM-YYYY
    - DD/MM/YYYY

    Args:
        date_input: Date string to parse

    Returns:
        Parsed date object or None if parsing fails

    Examples:
        >>> parse_date("2025-12-31")
        datetime.date(2025, 12, 31)
        >>> parse_date("12/31/2025")
        datetime.date(2025, 12, 31)
    """
    if not date_input or not date_input.strip():
        return None

    date_input = date_input.strip()

    # Try various date formats
    formats = [
        "%Y-%m-%d",  # ISO 8601
        "%Y/%m/%d",
        "%m-%d-%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%d/%m/%Y",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(date_input, fmt).date()
            return parsed
        except ValueError:
            continue

    return None


def parse_datetime(datetime_input: str) -> Optional[datetime]:
    """
    Parse a datetime string in various formats.

    Supported formats:
    - YYYY-MM-DD HH:MM
    - YYYY/MM/DD HH:MM
    - MM-DD-YYYY HH:MM
    - MM/DD/YYYY HH:MM

    Args:
        datetime_input: Datetime string to parse

    Returns:
        Parsed datetime object or None if parsing fails

    Examples:
        >>> parse_datetime("2025-12-31 14:30")
        datetime.datetime(2025, 12, 31, 14, 30)
    """
    if not datetime_input or not datetime_input.strip():
        return None

    datetime_input = datetime_input.strip()

    # Try various datetime formats
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%m-%d-%Y %H:%M",
        "%m/%d/%Y %H:%M",
        "%d-%m-%Y %H:%M",
        "%d/%m/%Y %H:%M",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(datetime_input, fmt)
            return parsed
        except ValueError:
            continue

    return None


def validate_date_input(date_input: str) -> tuple[bool, Optional[date], Optional[str]]:
    """
    Validate date input and return parsed date with error message.

    Args:
        date_input: Date string to validate

    Returns:
        Tuple of (is_valid, parsed_date, error_message)
        - is_valid: True if date is valid
        - parsed_date: Parsed date object or None
        - error_message: Error description or None

    Examples:
        >>> validate_date_input("2025-12-31")
        (True, datetime.date(2025, 12, 31), None)
        >>> validate_date_input("invalid")
        (False, None, "Invalid date format")
    """
    if not date_input or not date_input.strip():
        return False, None, "Date cannot be empty"

    parsed_date = parse_date(date_input)

    if parsed_date is None:
        return False, None, (
            "Invalid date format. Use: YYYY-MM-DD (e.g., 2025-12-31), "
            "or MM/DD/YYYY (e.g., 12/31/2025)"
        )

    return True, parsed_date, None


def validate_datetime_input(datetime_input: str) -> tuple[bool, Optional[datetime], Optional[str]]:
    """
    Validate datetime input and return parsed datetime with error message.

    Args:
        datetime_input: Datetime string to validate

    Returns:
        Tuple of (is_valid, parsed_datetime, error_message)
        - is_valid: True if datetime is valid
        - parsed_datetime: Parsed datetime object or None
        - error_message: Error description or None

    Examples:
        >>> validate_datetime_input("2025-12-31 14:30")
        (True, datetime.datetime(2025, 12, 31, 14, 30), None)
    """
    if not datetime_input or not datetime_input.strip():
        return False, None, "Date and time cannot be empty"

    parsed_datetime = parse_datetime(datetime_input)

    if parsed_datetime is None:
        return False, None, (
            "Invalid datetime format. Use: YYYY-MM-DD HH:MM (e.g., 2025-12-31 14:30)"
        )

    return True, parsed_datetime, None


def parse_recurrence_pattern(pattern_input: str) -> Optional[Dict[str, Any]]:
    """
    Parse recurrence pattern string into dictionary.

    Supported patterns:
    - daily
    - weekly
    - monthly
    - none

    Args:
        pattern_input: Recurrence pattern string (case-insensitive)

    Returns:
        Recurrence pattern dict or None for "none"

    Examples:
        >>> parse_recurrence_pattern("daily")
        {'type': 'daily'}
        >>> parse_recurrence_pattern("none")
        None
    """
    if not pattern_input or not pattern_input.strip():
        return None

    pattern_input = pattern_input.strip().lower()

    if pattern_input == "none":
        return None
    elif pattern_input == "daily":
        return {"type": "daily"}
    elif pattern_input == "weekly":
        return {"type": "weekly"}
    elif pattern_input == "monthly":
        return {"type": "monthly"}
    else:
        return None


def validate_recurrence_input(pattern_input: str) -> tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Validate recurrence pattern input and return parsed pattern with error message.

    Args:
        pattern_input: Recurrence pattern string to validate

    Returns:
        Tuple of (is_valid, parsed_pattern, error_message)
        - is_valid: True if pattern is valid
        - parsed_pattern: Parsed pattern dict or None
        - error_message: Error description or None

    Examples:
        >>> validate_recurrence_input("daily")
        (True, {'type': 'daily'}, None)
        >>> validate_recurrence_input("invalid")
        (False, None, "Invalid recurrence pattern")
    """
    if not pattern_input or not pattern_input.strip():
        return True, None, None  # Empty means no recurrence

    pattern_input = pattern_input.strip()

    parsed_pattern = parse_recurrence_pattern(pattern_input)

    if parsed_pattern is None and pattern_input.lower() != "none":
        return False, None, (
            "Invalid recurrence pattern. Use: daily, weekly, monthly, or none"
        )

    return True, parsed_pattern, None

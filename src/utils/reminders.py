"""
Reminder System - Utility Layer

Due date reminder logic and console output for advanced todo features.
"""

from datetime import date, timedelta
from typing import List, Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.domain.task import Task
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console(force_terminal=True, legacy_windows=False)


def is_overdue(task: Task) -> bool:
    """
    Check if a task is overdue.

    A task is overdue if:
    - It is not completed
    - It has a due date
    - The due date is before today

    Args:
        task: Task to check

    Returns:
        True if task is overdue, False otherwise

    Examples:
        >>> from datetime import date
        >>> task = Task(1, "Test", due_date=date(2024, 1, 1))
        >>> is_overdue(task)  # Assuming today is after 2024-01-01
        True
    """
    if task.completed:
        return False

    if task.due_date is None:
        return False

    return task.due_date < date.today()


def is_due_today(task: Task) -> bool:
    """
    Check if a task is due today.

    Args:
        task: Task to check

    Returns:
        True if task is due today, False otherwise

    Examples:
        >>> from datetime import date
        >>> task = Task(1, "Test", due_date=date.today())
        >>> is_due_today(task)
        True
    """
    if task.due_date is None:
        return False

    return task.due_date == date.today()


def is_due_soon(task: Task, days: int = 7) -> bool:
    """
    Check if a task is due within the specified number of days.

    Args:
        task: Task to check
        days: Number of days to look ahead (default: 7)

    Returns:
        True if task is due within the specified days, False otherwise

    Examples:
        >>> from datetime import date, timedelta
        >>> task = Task(1, "Test", due_date=date.today() + timedelta(days=3))
        >>> is_due_soon(task, 7)
        True
    """
    if task.due_date is None:
        return False

    today = date.today()
    future_date = today + timedelta(days=days)

    return today <= task.due_date <= future_date


def get_overdue_tasks(tasks: List[Task]) -> List[Task]:
    """
    Get all overdue tasks from a list.

    Args:
        tasks: List of tasks to filter

    Returns:
        List of overdue tasks
    """
    return [task for task in tasks if is_overdue(task)]


def get_tasks_due_today(tasks: List[Task]) -> List[Task]:
    """
    Get all tasks due today from a list.

    Args:
        tasks: List of tasks to filter

    Returns:
        List of tasks due today
    """
    return [task for task in tasks if is_due_today(task)]


def get_tasks_due_soon(tasks: List[Task], days: int = 7) -> List[Task]:
    """
    Get all tasks due within the specified number of days.

    Args:
        tasks: List of tasks to filter
        days: Number of days to look ahead (default: 7)

    Returns:
        List of tasks due soon
    """
    return [task for task in tasks if is_due_soon(task, days)]


def display_reminders(tasks: List[Task]):
    """
    Display reminders for tasks that are overdue, due today, or due soon.

    Shows:
    - Overdue tasks (red)
    - Tasks due today (yellow)
    - Tasks due within 7 days (cyan)

    Args:
        tasks: List of tasks to check for reminders
    """
    if not tasks:
        return

    # Get different categories of tasks
    overdue_tasks = get_overdue_tasks(tasks)
    today_tasks = get_tasks_due_today(tasks)
    soon_tasks = get_tasks_due_soon(tasks, days=7)

    # Don't display duplicates
    # (tasks that are also in today_tasks or soon_tasks)
    today_only_tasks = [t for t in today_tasks if not is_overdue(t)]
    soon_only_tasks = [t for t in soon_tasks
                      if not is_overdue(t)
                      and not is_due_today(t)]

    # Display reminders if any exist
    if not overdue_tasks and not today_only_tasks and not soon_only_tasks:
        return

    console.print()

    # Display overdue tasks
    if overdue_tasks:
        _display_overdue_reminders(overdue_tasks)

    # Display tasks due today
    if today_only_tasks:
        _display_today_reminders(today_only_tasks)

    # Display tasks due soon
    if soon_only_tasks:
        _display_soon_reminders(soon_only_tasks)


def _display_overdue_reminders(overdue_tasks: List[Task]):
    """
    Display overdue task reminders.

    Args:
        overdue_tasks: List of overdue tasks
    """
    console.print()
    title = f"[bold red]⚠️  OVERDUE TASKS ({len(overdue_tasks)})[/bold red]"

    # Create table for overdue tasks
    table = Table(
        title=title,
        show_header=True,
        header_style="bold red",
        border_style="red",
        title_style="bold red"
    )

    table.add_column("ID", style="bold white", justify="center", width=5)
    table.add_column("Title", style="bold red", width=25)
    table.add_column("Due Date", style="bold yellow", justify="center", width=12)

    for task in overdue_tasks:
        due_days_ago = (date.today() - task.due_date).days
        overdue_text = f"{task.due_date.isoformat()} ({due_days_ago}d ago)"

        table.add_row(
            str(task.id),
            task.title,
            overdue_text
        )

    console.print(table)


def _display_today_reminders(today_tasks: List[Task]):
    """
    Display tasks due today reminders.

    Args:
        today_tasks: List of tasks due today
    """
    console.print()
    title = f"[bold yellow]📅 DUE TODAY ({len(today_tasks)})[/bold yellow]"

    # Create table for today tasks
    table = Table(
        title=title,
        show_header=True,
        header_style="bold yellow",
        border_style="yellow",
        title_style="bold yellow"
    )

    table.add_column("ID", style="bold white", justify="center", width=5)
    table.add_column("Title", style="bold yellow", width=35)

    for task in today_tasks:
        table.add_row(str(task.id), task.title)

    console.print(table)


def _display_soon_reminders(soon_tasks: List[Task]):
    """
    Display tasks due soon reminders.

    Args:
        soon_tasks: List of tasks due soon
    """
    console.print()
    title = f"[bold cyan]📆 DUE SOON ({len(soon_tasks)})[/bold cyan]"

    # Create table for soon tasks
    table = Table(
        title=title,
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
        title_style="bold cyan"
    )

    table.add_column("ID", style="bold white", justify="center", width=5)
    table.add_column("Title", style="bold cyan", width=30)
    table.add_column("Due Date", style="bold white", justify="center", width=12)

    for task in soon_tasks:
        days_until = (task.due_date - date.today()).days

        if days_until == 1:
            due_text = f"{task.due_date.isoformat()} (tomorrow)"
        else:
            due_text = f"{task.due_date.isoformat()} ({days_until}d)"

        table.add_row(
            str(task.id),
            task.title,
            due_text
        )

    console.print(table)


def display_reminder_summary(tasks: List[Task]):
    """
    Display a summary of reminders (counts only, not detailed lists).

    Args:
        tasks: List of tasks to check for reminders
    """
    if not tasks:
        return

    overdue_count = len(get_overdue_tasks(tasks))
    today_count = len(get_tasks_due_today(tasks))
    soon_count = len(get_tasks_due_soon(tasks, days=7))

    if overdue_count == 0 and today_count == 0 and soon_count == 0:
        return

    console.print()
    summary_parts = []

    if overdue_count > 0:
        summary_parts.append(f"[bold red]{overdue_count} overdue[/bold red]")

    if today_count > 0:
        summary_parts.append(f"[bold yellow]{today_count} due today[/bold yellow]")

    if soon_count > 0:
        summary_parts.append(f"[bold cyan]{soon_count} due soon[/bold cyan]")

    summary = ", ".join(summary_parts)

    panel = Panel(
        f"[bold white]📌 {summary}[/bold white]",
        border_style="yellow",
        padding=(0, 2)
    )
    console.print(panel)

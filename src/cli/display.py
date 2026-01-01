"""
Display and Input Validation - CLI Presentation Layer

Output formatting and input validation per FR-011, FR-012, FR-026-FR-030, FR-033, FR-034.
Enhanced with rich library for beautiful terminal output.
Extended with priority display per FR-004 (Task Organization).
"""

from typing import List, Optional
from datetime import date
import sys
import os

# Add parent directory to path to import domain module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.domain.task import Task, TaskPriority

# Rich library imports for beautiful CLI
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich import print as rprint

# Initialize console with proper encoding for Windows
console = Console(force_terminal=True, legacy_windows=False)


def display_menu():
    """Display the main menu (FR-026) with rich styling. Extended with tag options (FR-006-FR-011) and advanced features."""
    console.print()  # Blank line

    # Create a beautiful table for menu options with perfect alignment
    table = Table(
        title="[bold magenta]TODO APP MENU[/bold magenta]",
        show_header=False,
        show_lines=False,
        border_style="cyan",
        padding=(0, 2),
        box=None  # Clean look without box borders
    )

    # Two columns: left and right menu options
    # Column widths set to accommodate longest text with proper spacing
    table.add_column("", width=28, justify="left")  # Left column
    table.add_column("", width=28, justify="left")  # Right column

    # Define menu options with rich formatting and colors
    # Left column (options 1, 3, 5, 7, 9, 11, 13)
    left_options = [
        "[bold cyan]➕  1. [/bold cyan][white]Add Task[/white]",
        "[bold cyan]📋  3. [/bold cyan][white]View Tasks[/white]",
        "[bold cyan]✅  5. [/bold cyan][white]Mark Complete[/white]",
        "[bold cyan]🏷️  7. [/bold cyan][white]Add Tag[/white]",
        "[bold cyan]🔄  9. [/bold cyan][white]Replace Tags[/white]",
        "[bold cyan]⚠️ 11. [/bold cyan][white]View Overdue[/white]",
        "[bold cyan]🔄 13. [/bold cyan][white]Set Recurrence[/white]",
    ]

    # Right column (options 2, 4, 6, 8, 10, 12, 14)
    right_options = [
        "[bold cyan]✏️  2. [/bold cyan][white]Update Task[/white]",
        "[bold cyan]❌  4. [/bold cyan][white]Delete Task[/white]",
        "[bold cyan]🔄  6. [/bold cyan][white]Mark Incomplete[/white]",
        "[bold cyan]❌  8. [/bold cyan][white]Remove Tag[/white]",
        "[bold cyan]🔍 10. [/bold cyan][white]Search Tasks[/white]",
        "[bold cyan]📅 12. [/bold cyan][white]View by Due Date[/white]",
        "[bold yellow]🚪 14. [/bold yellow][bold yellow]Exit[/bold yellow]",
    ]

    # Add rows to table (paired left and right options)
    for left, right in zip(left_options, right_options):
        table.add_row(left, right)

    # Wrap table in a panel for better visual framing
    panel = Panel(
        table,
        border_style="cyan",
        padding=(0, 1)
    )

    # Display the menu
    console.print(panel)


def display_task(task: Task):
    """
    Display a single task with all details (FR-012).
    Note: This function is now used internally by display_task_list.

    Args:
        task: Task to display
    """
    # This function is kept for compatibility but the actual display
    # is handled by the rich Table in display_task_list
    pass


def display_task_list(tasks: List[Task], sort_by: str = None):
    """
    Display all tasks in creation order (FR-011, FR-012, FR-014).
    Enhanced with rich Table for beautiful output.
    Extended with priority display per FR-004.
    Extended with due_date display and sort support (FR-020 through FR-024).

    Args:
        tasks: List of tasks to display
        sort_by: Optional sort criteria string for display purposes
    """
    if not tasks:
        display_empty_list_message()
        return

    console.print()  # Blank line

    # Build title with sort info
    title = "[bold magenta]YOUR TASKS[/bold magenta]"
    if sort_by:
        sort_text = {
            "title": "Title (A-Z)",
            "priority": "Priority (High → Medium → Low)",
            "due-date": "Due Date (oldest first)"
        }
        title += f" - Sorted by: [bold cyan]{sort_text.get(sort_by, sort_by)}[/bold cyan]"

    # Create a rich table
    table = Table(
        title=title,
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        title_style="bold magenta"
    )

    # Add columns (with due date, recurrence for Task Sorting feature, tags for FR-006)
    table.add_column("ID", style="bold white", justify="center", width=5)
    table.add_column("Title", style="bold cyan", width=18)
    table.add_column("Priority", justify="center", width=9)
    table.add_column("Due Date", justify="center", width=14)
    table.add_column("Recurrence", justify="center", width=12)
    table.add_column("Tags", style="cyan", width=15)
    table.add_column("Description", style="white", width=18)
    table.add_column("Status", justify="center", width=10)

    # Add rows
    for task in tasks:
        status_text = "[bold green]✅ Done[/bold green]" if task.completed else "[bold yellow]⏳ Pending[/bold yellow]"
        description = task.description if task.description else ""

        # Truncate long descriptions
        if len(description) > 18:
            description = description[:15] + "..."

        # Format priority with color coding
        if task.priority == TaskPriority.HIGH:
            priority_text = "[bold red]🔴 High[/bold red]"
        elif task.priority == TaskPriority.MEDIUM:
            priority_text = "[bold yellow]🟡 Med[/bold yellow]"
        else:  # LOW
            priority_text = "[bold green]🟢 Low[/bold green]"

        # Format due date with overdue highlighting
        from datetime import date as date_type
        if isinstance(task.due_date, date_type):
            from datetime import date as datetime_date
            # Check if task is overdue
            if not task.completed and task.due_date < datetime_date.today():
                due_date_text = f"[bold red]{task.due_date.isoformat()}[/bold red]"
            else:
                due_date_text = task.due_date.isoformat()
        else:
            due_date_text = ""

        # Format recurrence with visual indicator
        if task.recurrence_pattern:
            rec_type = task.recurrence_pattern.get('type', '').capitalize()
            recurrence_text = f"[bold magenta]🔄 {rec_type}[/bold magenta]"
        else:
            recurrence_text = ""

        # Format tags - display comma-separated with limited length (FR-006)
        tags_text = ", ".join(task.tags) if task.tags else ""
        if len(tags_text) > 15:
            tags_text = tags_text[:12] + "..."

        table.add_row(
            str(task.id),
            task.title,
            priority_text,
            due_date_text,
            recurrence_text,
            tags_text,
            description,
            status_text
        )

    # Display table in a panel
    console.print(table)

    # Display total count
    total_text = f"[bold white]📊 Total: {len(tasks)} task(s)[/bold white]"
    console.print(f"\n{total_text:^80}\n")


def display_empty_list_message():
    """Display message for empty task list (FR-013) with rich styling."""
    console.print()
    empty_panel = Panel(
        "[yellow]📭 No tasks found![/yellow]\n[cyan]Add your first task to get started.[/cyan]",
        title="[bold magenta]YOUR TASKS[/bold magenta]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(empty_panel)
    console.print()


def display_no_search_results(keyword: str):
    """
    Display message when search returns no matching tasks (FR-014) with rich styling.

    Args:
        keyword: The search keyword that found no matches
    """
    console.print()
    no_results_panel = Panel(
        f"[yellow]🔍 No tasks found matching '{keyword}'[/yellow]\n[cyan]Try a different keyword or add more tasks.[/cyan]",
        title="[bold magenta]SEARCH RESULTS[/bold magenta]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(no_results_panel)
    console.print()


def display_no_overdue_tasks():
    """Display message when there are no overdue tasks with rich styling."""
    console.print()
    no_overdue_panel = Panel(
        "[green]✨ No overdue tasks![/green]\n[cyan]All tasks are up to date. Keep up the good work![/cyan]",
        title="[bold magenta]OVERDUE TASKS[/bold magenta]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(no_overdue_panel)
    console.print()


def display_success(message: str):
    """
    Display success message (FR-029) with rich styling.

    Args:
        message: Success message to display
    """
    console.print()
    success_panel = Panel(
        f"[bold green]✅ {message}[/bold green]",
        border_style="green",
        padding=(0, 2)
    )
    console.print(success_panel)


def display_error(message: str):
    """
    Display error message (FR-030, FR-034) with rich styling.

    Args:
        message: Error message to display
    """
    console.print()
    error_panel = Panel(
        f"[bold red]❌ {message}[/bold red]",
        border_style="red",
        padding=(0, 2)
    )
    console.print(error_panel)


def read_menu_choice() -> Optional[int]:
    """
    Read and validate menu choice (FR-027) with rich styling.
    Extended to support options 1-14 (including tag, search, and advanced options).

    Returns:
        Valid menu choice (1-14) or None if invalid
    """
    try:
        choice = Prompt.ask("\n[bold cyan]👉 Enter your choice[/bold cyan]", default="")
        if not choice:
            return None

        choice_int = int(choice)
        if 1 <= choice_int <= 14:
            return choice_int
        else:
            display_error("Please enter a number between 1 and 14.")
            return None
    except ValueError:
        display_error("Please enter a valid number.")
        return None


def read_task_id(prompt: str) -> Optional[int]:
    """
    Read and validate task ID input with rich styling.

    Args:
        prompt: Prompt message to display

    Returns:
        Task ID as integer or None if invalid
    """
    try:
        value = Prompt.ask(f"\n[bold cyan]🔢 {prompt}[/bold cyan]", default="")
        if not value:
            display_error("Task ID cannot be empty.")
            return None

        task_id = int(value)
        if task_id <= 0:
            display_error("Task ID must be a positive number.")
            return None

        return task_id
    except ValueError:
        display_error("Please enter a valid task ID (number).")
        return None


def read_text(prompt: str, required: bool = False, emoji: str = "📝") -> Optional[str]:
    """
    Read text input with optional validation (FR-028) with rich styling.

    Args:
        prompt: Prompt message to display
        required: If True, rejects empty input
        emoji: Emoji to display before prompt (default: 📝)

    Returns:
        Input text or None if validation fails
    """
    styled_prompt = f"\n[bold cyan]{emoji} {prompt}[/bold cyan]"
    value = Prompt.ask(styled_prompt, default="").strip()

    if required and not value:
        display_error("This field is required and cannot be empty.")
        return None

    # For non-required fields, return empty string if nothing entered
    # For required fields, return the value (already validated as non-empty)
    return value if value else "" if not required else None


def validate_title(title: str) -> bool:
    """
    Validate task title (non-empty after strip).

    Args:
        title: Title to validate

    Returns:
        True if valid, False otherwise
    """
    return bool(title and title.strip())


def read_priority(prompt: str = "Enter priority") -> Optional[TaskPriority]:
    """
    Read and validate priority input (FR-001, FR-003).

    Args:
        prompt: Prompt message to display

    Returns:
        TaskPriority enum value or None if validation fails
    """
    try:
        styled_prompt = f"\n[bold cyan]🎯 {prompt} (high/medium/low)[/bold cyan]"
        value = Prompt.ask(styled_prompt, default="").strip()

        if not value:
            return None  # User wants to keep current value

        return TaskPriority.from_string(value)
    except ValueError as e:
        display_error(str(e))
        return None


def display_operation_header(title: str, emoji: str):
    """
    Display a header panel for an operation.

    Args:
        title: Title of the operation
        emoji: Emoji to display
    """
    console.print()
    header_panel = Panel(
        f"[bold white]{emoji} {title}[/bold white]",
        border_style="cyan",
        padding=(0, 2)
    )
    console.print(header_panel)


def display_current_values(task):
    """
    Display current task values in a styled panel.
    Extended with priority display per FR-004.
    Extended with due date and recurrence display for advanced features.

    Args:
        task: Task object to display
    """
    console.print("\n[bold yellow]Current Values:[/bold yellow]")
    values_text = f"[cyan]Title:[/cyan] {task.title}\n"
    values_text += f"[cyan]Description:[/cyan] {task.description if task.description else '(empty)'}\n"

    # Format priority with color
    if task.priority == TaskPriority.HIGH:
        priority_display = "[bold red]High[/bold red]"
    elif task.priority == TaskPriority.MEDIUM:
        priority_display = "[bold yellow]Medium[/bold yellow]"
    else:  # LOW
        priority_display = "[bold green]Low[/bold green]"

    values_text += f"[cyan]Priority:[/cyan] {priority_display}\n"

    # Display due date
    from datetime import date as date_type
    if isinstance(task.due_date, date_type):
        values_text += f"[cyan]Due Date:[/cyan] {task.due_date.isoformat()}\n"
    else:
        values_text += f"[cyan]Due Date:[/cyan] (not set)\n"

    # Display recurrence
    if task.recurrence_pattern:
        rec_type = task.recurrence_pattern.get('type', '').capitalize()
        values_text += f"[cyan]Recurrence:[/cyan] {rec_type}"
    else:
        values_text += f"[cyan]Recurrence:[/cyan] (not recurring)"

    values_panel = Panel(
        values_text,
        border_style="yellow",
        padding=(0, 2)
    )
    console.print(values_panel)


def read_date_input(prompt: str, required: bool = False) -> Optional[date]:
    """
    Read and validate date input.

    Args:
        prompt: Prompt message to display
        required: If True, rejects empty input

    Returns:
        Parsed date object or None if validation fails/not required

    Examples:
        >>> read_date_input("Enter due date")
        datetime.date(2025, 12, 31)
    """
    from src.utils.validators import validate_date_input
    from datetime import date as date_type

    while True:
        styled_prompt = f"\n[bold cyan]📅 {prompt} (YYYY-MM-DD, or press Enter to skip)[/bold cyan]"
        value = Prompt.ask(styled_prompt, default="").strip()

        if not value:
            if required:
                display_error("Due date is required.")
                continue
            return None

        is_valid, parsed_date, error_msg = validate_date_input(value)

        if is_valid:
            return parsed_date
        else:
            display_error(error_msg)


def read_recurrence_input(prompt: str, required: bool = False) -> Optional[dict]:
    """
    Read and validate recurrence pattern input.

    Args:
        prompt: Prompt message to display
        required: If True, rejects empty input

    Returns:
        Recurrence pattern dict or None if validation fails/not required

    Examples:
        >>> read_recurrence_input("Enter recurrence")
        {'type': 'daily'}
    """
    from src.utils.validators import validate_recurrence_input

    while True:
        styled_prompt = f"\n[bold cyan]🔄 {prompt} (daily/weekly/monthly, or press Enter for none)[/bold cyan]"
        value = Prompt.ask(styled_prompt, default="").strip()

        if not value:
            if required:
                display_error("Recurrence pattern is required.")
                continue
            return None

        is_valid, parsed_pattern, error_msg = validate_recurrence_input(value)

        if is_valid:
            return parsed_pattern
        else:
            display_error(error_msg)

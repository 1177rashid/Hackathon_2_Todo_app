"""
Display and Input Validation - CLI Presentation Layer

Output formatting and input validation per FR-011, FR-012, FR-026-FR-030, FR-033, FR-034.
Enhanced with rich library for beautiful terminal output.
"""

from typing import List, Optional
import sys
import os

# Add parent directory to path to import domain module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.domain.task import Task

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
    """Display the main menu (FR-026) with rich styling."""
    console.print()  # Blank line

    # Create menu options in two columns
    menu_items = [
        Text("➕ 1. Add Task", style="bold white"),
        Text("✏️  3. Update Task", style="bold white"),
        Text("📋 2. View Tasks", style="bold white"),
        Text("❌ 4. Delete Task", style="bold white"),
        Text("✅ 5. Mark Complete", style="bold white"),
        Text("🔄 6. Mark Incomplete", style="bold white"),
        Text("🚪 7. Exit", style="bold yellow"),
    ]

    # Create two-column layout
    col1 = "\n".join([str(menu_items[0]), str(menu_items[2]), str(menu_items[4])])
    col2 = "\n".join([str(menu_items[1]), str(menu_items[3]), str(menu_items[5])])

    # Build menu content
    menu_content = f"  {menu_items[0].plain}         {menu_items[1].plain}\n"
    menu_content += f"  {menu_items[2].plain}        {menu_items[3].plain}\n"
    menu_content += f"  {menu_items[4].plain}    {menu_items[5].plain}\n"
    menu_content += f"  {menu_items[6].plain}"

    # Display menu in a panel
    panel = Panel(
        menu_content,
        title="[bold magenta]TODO APP MENU[/bold magenta]",
        border_style="cyan",
        padding=(1, 2)
    )
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


def display_task_list(tasks: List[Task]):
    """
    Display all tasks in creation order (FR-011, FR-012, FR-014).
    Enhanced with rich Table for beautiful output.

    Args:
        tasks: List of tasks to display
    """
    if not tasks:
        display_empty_list_message()
        return

    console.print()  # Blank line

    # Create a rich table
    table = Table(
        title="[bold magenta]YOUR TASKS[/bold magenta]",
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        title_style="bold magenta"
    )

    # Add columns
    table.add_column("ID", style="bold white", justify="center", width=6)
    table.add_column("Title", style="bold cyan", width=25)
    table.add_column("Description", style="white", width=30)
    table.add_column("Status", justify="center", width=12)

    # Add rows
    for task in tasks:
        status_text = "[bold green]✅ Done[/bold green]" if task.completed else "[bold yellow]⏳ Pending[/bold yellow]"
        description = task.description if task.description else ""

        # Truncate long descriptions
        if len(description) > 30:
            description = description[:27] + "..."

        table.add_row(
            str(task.id),
            task.title,
            description,
            status_text
        )

    # Display table in a panel
    console.print(table)

    # Display total count
    total_text = f"[bold white]📊 Total: {len(tasks)} task(s)[/bold white]"
    console.print(f"\n{total_text:^60}\n")


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

    Returns:
        Valid menu choice (1-7) or None if invalid
    """
    try:
        choice = Prompt.ask("\n[bold cyan]👉 Enter your choice[/bold cyan]", default="")
        if not choice:
            return None

        choice_int = int(choice)
        if 1 <= choice_int <= 7:
            return choice_int
        else:
            display_error("Please enter a number between 1 and 7.")
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

    Args:
        task: Task object to display
    """
    console.print("\n[bold yellow]Current Values:[/bold yellow]")
    values_text = f"[cyan]Title:[/cyan] {task.title}\n"
    values_text += f"[cyan]Description:[/cyan] {task.description if task.description else '(empty)'}"

    values_panel = Panel(
        values_text,
        border_style="yellow",
        padding=(0, 2)
    )
    console.print(values_panel)

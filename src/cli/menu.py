"""
Menu System - CLI Presentation Layer

Main menu loop and operation dispatch per FR-026, FR-027, FR-031, FR-032.
Enhanced with rich library for beautiful CLI.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.state.task_store import TaskStore
from src.cli.display import display_menu, read_menu_choice, display_error
from src.cli.handlers import (
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_mark_complete,
    handle_mark_incomplete
)
from rich.console import Console
from rich.panel import Panel

console = Console(force_terminal=True, legacy_windows=False)


def run_menu(store: TaskStore):
    """
    Run the main menu loop (FR-026, FR-027, FR-031, FR-032).

    Args:
        store: TaskStore instance

    The menu loop:
    - Displays menu (FR-026)
    - Reads user choice (FR-027)
    - Dispatches to appropriate handler
    - Returns to menu after each operation (FR-031)
    - Exits cleanly on option 7 (FR-032)
    """
    while True:
        try:
            # Display menu (FR-026)
            display_menu()

            # Read user choice (FR-027)
            choice = read_menu_choice()

            if choice is None:
                # Invalid input was already handled by read_menu_choice
                continue

            # Dispatch to handler based on choice
            if choice == 1:
                handle_add_task(store)
            elif choice == 2:
                handle_view_tasks(store)
            elif choice == 3:
                handle_update_task(store)
            elif choice == 4:
                handle_delete_task(store)
            elif choice == 5:
                handle_mark_complete(store)
            elif choice == 6:
                handle_mark_incomplete(store)
            elif choice == 7:
                # Exit cleanly (FR-032, User Story 6)
                console.print()
                goodbye_panel = Panel(
                    "[bold cyan]👋 Thank you for using Todo App![/bold cyan]\n[yellow]Stay organized and productive![/yellow]",
                    border_style="magenta",
                    padding=(0, 2)
                )
                console.print(goodbye_panel)
                console.print()
                break

            # Return to menu after each operation (FR-031)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print()
            goodbye_panel = Panel(
                "[bold cyan]👋 Thank you for using Todo App![/bold cyan]\n[yellow]Stay organized and productive![/yellow]",
                border_style="magenta",
                padding=(0, 2)
            )
            console.print(goodbye_panel)
            console.print()
            break
        except Exception as e:
            # Catch unexpected errors (FR-033, FR-034)
            display_error(f"An unexpected error occurred: {str(e)}")
            # Continue to menu (don't crash)

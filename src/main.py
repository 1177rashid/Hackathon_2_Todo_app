"""
Main Entry Point - Phase I In-Memory CLI Todo Application

Application entry point per FR-032, FR-033, User Story 6.
Enhanced with rich library for beautiful CLI.
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from state.task_store import TaskStore
from cli.menu import run_menu
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console(force_terminal=True, legacy_windows=False)


def display_welcome_banner():
    """Display a beautiful welcome banner using rich."""
    # Create ASCII art title
    title = Text()
    title.append("████████╗ ██████╗ ██████╗  ██████╗ \n", style="bold magenta")
    title.append("╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗\n", style="bold magenta")
    title.append("   ██║   ██║   ██║██║  ██║██║   ██║\n", style="bold magenta")
    title.append("   ██║   ██║   ██║██║  ██║██║   ██║\n", style="bold magenta")
    title.append("   ██║   ╚██████╔╝██████╔╝╚██████╔╝\n", style="bold magenta")
    title.append("   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ ", style="bold magenta")

    # Create subtitle
    subtitle = Text("\n\n📝 Organize Your Life, One Task at a Time 📝\n", style="bold cyan", justify="center")
    subtitle.append("Version 1.0.0", style="cyan")

    # Combine title and subtitle
    banner_content = Text()
    banner_content.append(title)
    banner_content.append(subtitle)

    # Create panel
    banner = Panel(
        banner_content,
        border_style="cyan",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(banner)
    console.print("\n")


def main():
    """
    Application entry point.

    Creates TaskStore and runs the main menu loop.
    Catches unexpected errors gracefully (FR-033).
    """
    try:
        # Display welcome banner
        display_welcome_banner()

        # Create task store instance
        store = TaskStore()

        # Run main menu loop
        run_menu(store)

    except Exception as e:
        # Catch any unexpected errors (FR-033, FR-034)
        console.print(f"\n[bold red]✗ Fatal error: {str(e)}[/bold red]")
        console.print("[yellow]The application will now exit.[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()

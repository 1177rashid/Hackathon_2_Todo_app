"""
Main Entry Point - CLI Todo Application

Initializes the task store and runs the main menu loop.
Integrates reminder system for advanced features.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.state.task_store import TaskStore
from src.cli.menu import run_menu
from src.utils.reminders import display_reminders


def main():
    """
    Main entry point for the Todo CLI application.

    1. Initializes the task store
    2. Displays reminders for overdue/due tasks
    3. Runs the main menu loop
    """
    # Initialize task store
    store = TaskStore()

    # Display reminders at startup (advanced features)
    tasks = store.get_all_tasks()
    if tasks:
        display_reminders(tasks)

    # Run main menu loop
    run_menu(store)


if __name__ == "__main__":
    main()

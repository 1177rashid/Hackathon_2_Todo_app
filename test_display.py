"""
Quick test script to verify rich display functions work correctly.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from domain.task import Task
from cli.display import (
    display_menu,
    display_task_list,
    display_empty_list_message,
    display_success,
    display_error,
    display_operation_header
)

def test_display():
    """Test all display functions."""
    print("\n" + "="*60)
    print("Testing Rich CLI Display Functions")
    print("="*60)

    # Test 1: Welcome and Menu
    print("\n[TEST 1] Displaying Main Menu...")
    display_menu()
    input("\nPress Enter to continue...")

    # Test 2: Empty List
    print("\n[TEST 2] Displaying Empty Task List...")
    display_empty_list_message()
    input("\nPress Enter to continue...")

    # Test 3: Task List with Data
    print("\n[TEST 3] Displaying Task List with Data...")
    tasks = [
        Task(1, "Buy groceries", "Milk, eggs, bread"),
        Task(2, "Finish project", "Complete Phase 1 implementation"),
        Task(3, "Call dentist", ""),
    ]
    tasks[0].completed = True  # Mark first task as complete
    display_task_list(tasks)
    input("\nPress Enter to continue...")

    # Test 4: Success Message
    print("\n[TEST 4] Displaying Success Message...")
    display_success("Task created with ID: 1")
    input("\nPress Enter to continue...")

    # Test 5: Error Message
    print("\n[TEST 5] Displaying Error Message...")
    display_error("Task with ID 99 not found.")
    input("\nPress Enter to continue...")

    # Test 6: Operation Headers
    print("\n[TEST 6] Displaying Operation Headers...")
    display_operation_header("ADD NEW TASK", "➕")
    input("\nPress Enter to continue...")

    display_operation_header("UPDATE TASK", "✏️")
    input("\nPress Enter to continue...")

    display_operation_header("DELETE TASK", "❌")
    input("\nPress Enter to continue...")

    display_operation_header("MARK TASK COMPLETE", "✅")
    input("\nPress Enter to continue...")

    print("\n" + "="*60)
    print("All display tests completed successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_display()

"""
Test script for advanced todo features (recurrence, sorting, filtering).

Validates:
- Recurrence pattern validation
- Next due date calculation with edge cases
- Task completion with recurrence generation
- Sorting by due date
- Overdue task detection
"""

import sys
import os
from datetime import date, timedelta

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.state.task_store import TaskStore
from src.state.recurrence_policy import validate_recurrence_pattern, calculate_next_due_date


def test_recurrence_validation():
    """Test recurrence pattern validation."""
    print("Testing recurrence pattern validation...")

    # Valid patterns
    assert validate_recurrence_pattern(None) == True
    assert validate_recurrence_pattern({'type': 'daily'}) == True
    assert validate_recurrence_pattern({'type': 'weekly'}) == True
    assert validate_recurrence_pattern({'type': 'monthly'}) == True

    # Invalid patterns
    assert validate_recurrence_pattern({'type': 'invalid'}) == False
    assert validate_recurrence_pattern({}) == False
    assert validate_recurrence_pattern('string') == False
    assert validate_recurrence_pattern(123) == False

    print("  - Recurrence validation: PASSED")


def test_next_due_date_calculation():
    """Test next due date calculation for each recurrence type."""
    print("\nTesting next due date calculation...")

    # Daily recurrence
    base_date = date(2025, 1, 15)
    next_daily = calculate_next_due_date(base_date, {'type': 'daily'})
    assert next_daily == date(2025, 1, 16)
    print(f"  - Daily: {base_date} -> {next_daily}: PASSED")

    # Weekly recurrence
    next_weekly = calculate_next_due_date(base_date, {'type': 'weekly'})
    assert next_weekly == date(2025, 1, 22)
    print(f"  - Weekly: {base_date} -> {next_weekly}: PASSED")

    # Monthly recurrence (normal case)
    next_monthly = calculate_next_due_date(base_date, {'type': 'monthly'})
    assert next_monthly == date(2025, 2, 15)
    print(f"  - Monthly (normal): {base_date} -> {next_monthly}: PASSED")

    # Monthly recurrence (edge case: Jan 31 -> Feb 28/29)
    jan_31 = date(2025, 1, 31)
    feb_next = calculate_next_due_date(jan_31, {'type': 'monthly'})
    assert feb_next == date(2025, 2, 28)
    print(f"  - Monthly (Jan 31 edge): {jan_31} -> {feb_next}: PASSED")

    # Monthly recurrence (leap year test)
    jan_31_2024 = date(2024, 1, 31)
    feb_2024 = calculate_next_due_date(jan_31_2024, {'type': 'monthly'})
    assert feb_2024 == date(2024, 2, 29)
    print(f"  - Monthly (leap year): {jan_31_2024} -> {feb_2024}: PASSED")


def test_task_creation_with_recurrence():
    """Test creating tasks with recurrence patterns."""
    print("\nTesting task creation with recurrence...")

    store = TaskStore()

    # Non-recurring task (backward compatibility)
    task1 = store.add_task("Basic task", "No recurrence")
    assert task1.recurrence_pattern is None
    assert task1.due_date is None
    print(f"  - Basic task created (ID: {task1.id}): PASSED")

    # Recurring daily task
    task2 = store.add_task(
        "Daily meeting",
        "Standup meeting",
        due_date=date(2025, 1, 15),
        recurrence_pattern={'type': 'daily'}
    )
    assert task2.recurrence_pattern == {'type': 'daily'}
    assert task2.due_date == date(2025, 1, 15)
    print(f"  - Daily recurring task created (ID: {task2.id}): PASSED")

    # Recurring weekly task with tags
    task3 = store.add_task(
        "Weekly review",
        "Code review session",
        due_date=date(2025, 1, 20),
        tags=['work', 'review'],
        recurrence_pattern={'type': 'weekly'}
    )
    assert task3.recurrence_pattern == {'type': 'weekly'}
    assert task3.tags == ['work', 'review']
    print(f"  - Weekly recurring task with tags created (ID: {task3.id}): PASSED")

    # Invalid recurrence pattern should raise error
    try:
        store.add_task(
            "Invalid task",
            recurrence_pattern={'type': 'invalid'}
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid recurrence pattern" in str(e)
        print(f"  - Invalid pattern rejected: PASSED")


def test_complete_task_with_recurrence():
    """Test completing tasks triggers recurrence generation."""
    print("\nTesting task completion with recurrence...")

    store = TaskStore()

    # Create non-recurring task
    task1 = store.add_task("One-time task", "No recurrence")
    new_task = store.complete_task(task1.id)
    assert new_task is None
    assert task1.completed == True
    print(f"  - Non-recurring task completion: PASSED")

    # Create daily recurring task
    task2 = store.add_task(
        "Daily check",
        "Check status daily",
        due_date=date(2025, 1, 15),
        recurrence_pattern={'type': 'daily'}
    )

    # Complete the task
    new_task = store.complete_task(task2.id)

    # Original task should be marked complete
    assert task2.completed == True

    # New task should be created with next due date
    assert new_task is not None
    assert new_task.id != task2.id
    assert new_task.title == task2.title
    assert new_task.description == task2.description
    assert new_task.completed == False
    assert new_task.due_date == date(2025, 1, 16)
    assert new_task.recurrence_pattern == task2.recurrence_pattern
    print(f"  - Daily recurrence: {task2.id} completed -> {new_task.id} created: PASSED")

    # Complete again to generate second instance
    new_task2 = store.complete_task(new_task.id)
    assert new_task2 is not None
    assert new_task2.due_date == date(2025, 1, 17)
    print(f"  - Second recurrence: {new_task.id} completed -> {new_task2.id} created: PASSED")

    # Test monthly recurrence edge case
    task3 = store.add_task(
        "Monthly report",
        "End of month report",
        due_date=date(2025, 1, 31),
        recurrence_pattern={'type': 'monthly'}
    )

    new_task3 = store.complete_task(task3.id)
    assert new_task3.due_date == date(2025, 2, 28)
    print(f"  - Monthly edge case (Jan 31 -> Feb 28): PASSED")

    # Test that recurring task without due date raises error
    task4 = store.add_task(
        "No due date",
        recurrence_pattern={'type': 'daily'}
    )
    try:
        store.complete_task(task4.id)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must have a due date" in str(e)
        print(f"  - Recurring without due date rejected: PASSED")


def test_sorting_by_due_date():
    """Test sorting tasks by due date."""
    print("\nTesting sorting by due date...")

    store = TaskStore()

    # Create tasks with various due dates and no due dates
    task1 = store.add_task("Task 1", due_date=date(2025, 1, 20))
    task2 = store.add_task("Task 2", due_date=date(2025, 1, 10))
    task3 = store.add_task("Task 3", due_date=None)
    task4 = store.add_task("Task 4", due_date=date(2025, 1, 15))
    task5 = store.add_task("Task 5", due_date=None)

    # Sort by due date
    sorted_tasks = store.get_sorted_by_due_date()

    # Verify order: tasks with due dates first (ascending), then tasks without
    assert sorted_tasks[0] == task2  # Jan 10
    assert sorted_tasks[1] == task4  # Jan 15
    assert sorted_tasks[2] == task1  # Jan 20
    assert sorted_tasks[3] == task3  # None (first in creation order)
    assert sorted_tasks[4] == task5  # None (second in creation order)

    print(f"  - Sorted order: {', '.join(f'#{t.id} ({t.due_date})' for t in sorted_tasks)}: PASSED")


def test_overdue_tasks():
    """Test detection of overdue tasks."""
    print("\nTesting overdue task detection...")

    store = TaskStore()

    today = date.today()

    # Create tasks with various states
    task1 = store.add_task("Overdue", due_date=today - timedelta(days=5))
    task2 = store.add_task("Due today", due_date=today)
    task3 = store.add_task("Future", due_date=today + timedelta(days=5))
    task4 = store.add_task("Overdue completed", due_date=today - timedelta(days=3))
    task5 = store.add_task("No due date", due_date=None)

    # Mark one overdue task as complete
    task4.completed = True

    # Get overdue tasks
    overdue = store.get_overdue_tasks()

    # Only task1 should be overdue (incomplete, due date in past)
    assert len(overdue) == 1
    assert task1 in overdue
    assert task2 not in overdue  # Due today is not overdue
    assert task3 not in overdue  # Future
    assert task4 not in overdue  # Completed
    assert task5 not in overdue  # No due date

    print(f"  - Overdue tasks: {len(overdue)} found (expected 1): PASSED")


def test_backward_compatibility():
    """Test that existing operations still work."""
    print("\nTesting backward compatibility...")

    store = TaskStore()

    # Basic CRUD operations
    task = store.add_task("Basic task", "Description", priority="high")
    assert task.priority.value == "high"

    retrieved = store.get_task(task.id)
    assert retrieved == task

    updated = store.update_task(task.id, title="Updated title")
    assert updated == True
    assert task.title == "Updated title"

    deleted = store.delete_task(task.id)
    assert deleted == True
    assert store.get_task(task.id) is None

    # Mark complete (non-recurring)
    task2 = store.add_task("Another task")
    completed = store.mark_complete(task2.id)
    assert completed == True
    assert task2.completed == True

    # Search
    task3 = store.add_task("Search test", "Find me")
    results = store.search_tasks("find")
    assert task3 in results

    # Tags
    task4 = store.add_task("Tag test")
    store.add_tag(task4.id, "important")
    assert "important" in task4.tags

    print(f"  - All existing operations functional: PASSED")


def run_all_tests():
    """Run all advanced feature tests."""
    print("=" * 60)
    print("ADVANCED TODO FEATURES TEST SUITE")
    print("=" * 60)

    try:
        test_recurrence_validation()
        test_next_due_date_calculation()
        test_task_creation_with_recurrence()
        test_complete_task_with_recurrence()
        test_sorting_by_due_date()
        test_overdue_tasks()
        test_backward_compatibility()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        return True

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

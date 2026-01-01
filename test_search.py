"""
Test script to verify Keyword Search functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.state.task_store import TaskStore
from src.domain.task import Task

def test_search():
    """Test search functionality with sample tasks."""
    print("Testing Keyword Search Feature")
    print("=" * 50)

    # Create task store
    store = TaskStore()

    # Add test tasks
    task1 = store.add_task("Submit quarterly report", "Complete Q4 financial summary")
    task2 = store.add_task("Buy groceries", "Get milk, bread, and eggs")
    task3 = store.add_task("Review contract", "Check legal terms")
    task4 = store.add_task("Call client", "Discuss project scope")
    task5 = store.add_task("Update documentation", "Review API docs")

    print(f"\nCreated {len(store.get_all_tasks())} test tasks\n")

    # Test 1: Search for "report" (in title)
    print("Test 1: Search for 'report' (in title)")
    results = store.search_tasks("report")
    print(f"  Found {len(results)} task(s):")
    for task in results:
        print(f"    - ID {task.id}: {task.title}")
    assert len(results) == 1, "Should find 1 task"
    assert results[0].id == 1, "Should find task 1"
    print("  PASS")

    # Test 2: Search for "GROCERIES" (uppercase in description)
    print("\nTest 2: Search for 'GROCERIES' (uppercase in description)")
    results = store.search_tasks("GROCERIES")
    print(f"  Found {len(results)} task(s):")
    for task in results:
        print(f"    - ID {task.id}: {task.title}")
    assert len(results) == 1, "Should find 1 task"
    assert results[0].id == 2, "Should find task 2"
    print("  PASS")

    # Test 3: Search for "review" (multiple matches)
    print("\nTest 3: Search for 'review' (multiple matches)")
    results = store.search_tasks("review")
    print(f"  Found {len(results)} task(s):")
    for task in results:
        print(f"    - ID {task.id}: {task.title}")
    assert len(results) == 2, "Should find 2 tasks"
    print("  PASS")

    # Test 4: Search for non-existent keyword
    print("\nTest 4: Search for 'nonexistent' (no matches)")
    results = store.search_tasks("nonexistent")
    print(f"  Found {len(results)} task(s):")
    assert len(results) == 0, "Should find 0 tasks"
    print("  PASS")

    # Test 5: Case-insensitive search
    print("\nTest 5: Search for 'QUARTERLY' (uppercase in title)")
    results = store.search_tasks("QUARTERLY")
    print(f"  Found {len(results)} task(s):")
    for task in results:
        print(f"    - ID {task.id}: {task.title}")
    assert len(results) == 1, "Should find 1 task"
    print("  PASS")

    print("\n" + "=" * 50)
    print("All search tests PASSED!")
    print("Keyword Search feature is working correctly.")

if __name__ == "__main__":
    test_search()

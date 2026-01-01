---
id: 006
title: advanced-todo-implementation
stage: spec
date: 2025-12-31
surface: agent
model: claude-sonnet-4.5
feature: 001-todo-organization
branch: 001-todo-organization
user: Maryam
command: Implement the advanced todo features in-memory state management
labels: [implementation,recurrence,sorting,filtering]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - src/domain/task.py
 - src/state/task_store.py
 - src/state/recurrence_policy.py
 - src/state/__init__.py
 - test_advanced_features.py
tests:
 - test_advanced_features.py (all 7 test suites passed)
 - test_search.py (backward compatibility verified)
---

## Prompt

Implement the advanced todo features in-memory state management according to the plan:

1. Extend `src/state/task_store.py` to support:
   - New fields: due_date (datetime | None), recurrence_pattern (dict | None)
   - New operation: complete_task() triggers recurrence regeneration
   - Sorting: get_sorted_by_due_date() method
   - Filtering: get_overdue_tasks() method

2. Implement recurrence policy (following recurrence_policy_engine skill):
   - Allowed patterns: daily, weekly, monthly, None
   - Due date calculation: daily (+1 day), weekly (+7 days), monthly (+1 month with edge case handling)
   - On completion: create new task instance with copied properties (title, description, priority, tags, recurrence_pattern) and calculated next_due_date
   - Edge cases: Feb 30 rejected, Jan 31 -> Feb 28/29 adjustment

3. Maintain backward compatibility:
   - All existing operations (add, view, update, delete) work unchanged
   - New fields default to None for non-Advanced tasks
   - Basic and Intermediate features remain fully functional

Follow the existing code structure and patterns. Use only Python standard library (datetime, not dateutil).

## Response snapshot

Successfully implemented advanced todo features with full backward compatibility:

**Domain Layer (src/domain/task.py):**
- Added recurrence_pattern parameter to Task class (Optional[Dict[str, Any]])
- Updated __repr__ to include recurrence_pattern
- Maintained all existing invariants

**State Management (src/state/task_store.py):**
- Extended add_task() to accept tags and recurrence_pattern parameters
- Added complete_task() method: marks task complete and generates next instance for recurring tasks
- Added get_sorted_by_due_date() method: returns tasks sorted by due date (ascending), tasks without due dates at end
- Added get_overdue_tasks() method: returns incomplete tasks with due dates in the past
- Validates recurrence_pattern on creation (allowed: None, daily, weekly, monthly)

**Recurrence Policy Engine (src/state/recurrence_policy.py):**
- validate_recurrence_pattern(): validates pattern structure
- calculate_next_due_date(): calculates next occurrence
  - daily: +1 day
  - weekly: +7 days
  - monthly: +1 month with edge case handling (Jan 31 -> Feb 28/29)
- Uses only Python standard library (datetime, calendar.monthrange)

**Testing (test_advanced_features.py):**
- test_recurrence_validation(): validates all pattern types
- test_next_due_date_calculation(): tests all recurrence types including edge cases (Jan 31, leap year)
- test_task_creation_with_recurrence(): creates tasks with recurrence, validates errors
- test_complete_task_with_recurrence(): verifies recurrence generation on completion
- test_sorting_by_due_date(): validates sorting with/without due dates
- test_overdue_tasks(): filters incomplete tasks past due date
- test_backward_compatibility(): confirms all existing operations work unchanged

**Results:**
- All 7 test suites PASSED
- Backward compatibility verified with existing test_search.py
- Edge cases handled: Jan 31 -> Feb 28/29, recurring tasks require due_date, invalid patterns rejected

## Outcome

- ✅ Impact: Advanced todo features fully implemented (recurrence, sorting, overdue detection) with complete backward compatibility maintained
- 🧪 Tests: All 7 test suites passed; backward compatibility verified
- 📁 Files: Extended Task domain, TaskStore with 3 new methods, created RecurrencePolicy engine, comprehensive test suite
- 🔁 Next prompts: CLI handler integration for advanced features, display layer updates for recurrence/sorting
- 🧠 Reflection: Implementation follows existing patterns; recurrence policy properly isolated; edge cases handled with standard library only

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All tests PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): None (implementation complete and tested)

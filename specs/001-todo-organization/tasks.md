# Implementation Tasks: Todo Organization & Usability

**Feature**: 001-todo-organization | **Date**: 2025-12-31 | **Status**: Draft

**Branch**: `001-todo-organization`
**Plan**: [plan.md](./plan.md)
**Spec**: [spec.md](./spec.md)

## Dependencies

| User Story | Depends On |
|-----------|-----------|
| US1 (Task Priority) | None |
| US2 (Task Tagging) | None |
| US3 (Keyword Search) | None |
| US4 (Task Filtering) | US1, US2, US3 |
| US5 (Task Sorting) | None |

---

## Phase 1: Setup

**Goal**: Initialize project structure and supporting infrastructure for all user stories.

**Independent Test**: Can be verified by checking file structure, imports work correctly, pytest runs successfully. Delivers foundation for all subsequent phases without blocking stories.

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Add Priority enum to src/models/task.py (dataclass extension)
- [ ] T003 Create validator module at src/lib/validators.py
- [ ] T004 Create constants module at src/lib/constants.py
- [ ] T005 Update TaskService to support priority, tags, due_date in create/update
- [ ] T006 Run existing test suite to verify backward compatibility

**Tests**: Run `pytest tests/` after T006 to confirm no regressions.

---

## Phase 2: US1 - Task Priority Management

**Goal**: Implement task priority assignment (high/medium/low), default priority handling, and validation per FR-001 through FR-005 and US1 acceptance scenarios.

**Independent Test**: Can create tasks with different priorities, list tasks to verify priority display, update task priority without modifying other fields. Delivers core organization value independently of tagging/filtering/sorting features.

- [ ] T007 [P] [US1] Add --priority argument to add-task CLI command with choices (high/medium/low)
- [ ] T008 [P] [US1] Add --priority argument to update-task CLI command (optional)
- [ ] T009 [P] [US1] Implement validate_priority() in validators.py to reject invalid values
- [ ] T010 [US1] Add priority error message to constants.py listing valid options
- [ ] T011 [US1] Update TaskService.create() to apply default Priority.MEDIUM (FR-002)
- [ ] T012 [US1] Update TaskService.create() to validate priority using validate_priority()
- [ ] T013 [US1] Update TaskService.update() to support priority updates (FR-005)
- [ ] T014 [US1] Extend display.format_task() to show priority level with visual indicator
- [ ] T015 [US1] Add unit test for priority validation (invalid values rejected with error)
- [ ] T016 [US1] Add integration test for task creation with priority (default medium)
- [ ] T017 [US1] Add integration test for task creation with explicit priority
- [ ] T018 [US1] Add integration test for task priority update (other fields unchanged)

**Tests**:
- Unit: `pytest tests/unit/ -k priority`
- Integration: `pytest tests/integration/test_cli_commands.py::test_priority`
- Verify FR-001, FR-002, FR-003, FR-004, FR-005 satisfied

---

## Phase 3: US2 - Task Tagging

**Goal**: Implement task tags (add/remove/replace), duplicate prevention, and independence from completion status per FR-006 through FR-011 and US2 acceptance scenarios.

**Independent Test**: Can add tags to tasks, list tasks to verify tag display, add/remove/replace tags, verify duplicate prevention. Delivers organization value independently of priority/searching/filtering/sorting.

- [ ] T019 [P] [US2] Add --tags argument to add-task CLI command (comma-separated list)
- [ ] T020 [US2] Add --tags argument to update-task CLI command with mode (add/remove/replace)
- [ ] T021 [P] [US2] Implement validate_tags() in validators.py to prevent duplicates, reject empty strings
- [ ] T022 [US2] Update TaskService.create() to accept and validate tags
- [ ] T023 [US2] Update TaskService.update() to support add/remove/replace tag operations (FR-008, FR-009, FR-010)
- [ ] T024 [US2] Ensure completion_status updates independently of tags (FR-011)
- [ ] T025 [US2] Extend display.format_task() to show tags as comma-separated list
- [ ] T026 [P] [US2] Add unit test for tag validation (duplicates prevented, empty strings rejected)
- [ ] T027 [US2] Add unit test for tag add operation
- [ ] T028 [US2] Add unit test for tag remove operation
- [ ] T029 [US2] Add unit test for tag replace operation
- [ ] T030 [US2] Add integration test for task creation with tags
- [ ] T031 [US2] Add integration test for tag add to existing task
- [ ] T032 [US2] Add integration test for tag remove from existing task
- [ ] T033 [US2] Add integration test for tag replace on existing task
- [ ] T034 [US2] Add integration test for completion status toggle (tags unaffected)

**Tests**:
- Unit: `pytest tests/unit/ -k tag`
- Integration: `pytest tests/integration/test_cli_commands.py::test_tags`
- Verify FR-006, FR-007, FR-008, FR-009, FR-010, FR-011 satisfied

---

## Phase 4: US3 - Keyword Search

**Goal**: Implement case-insensitive keyword search across task title and description, with friendly message for no results per FR-012 through FR-014 and US3 acceptance scenarios.

**Independent Test**: Can search for various keywords in titles/descriptions, verify case-insensitive matching, test empty results handling. Delivers usability value independently of priority/tagging/filtering/sorting.

- [ ] T035 [P] [US3] Add --search argument to list-tasks CLI command (keyword search)
- [ ] T036 [US3] Implement search-tasks CLI command (dedicated search interface)
- [ ] T037 [P] [US3] Implement filter_service.py with SearchQuery dataclass
- [ ] T038 [P] [US3] Implement search_tasks() in filter_service.py (title/description matching, case-insensitive)
- [ ] T039 [US3] Add "No tasks found matching '{keyword}'" message for empty search results (FR-014)
- [ ] T040 [P] [US3] Add unit test for search across title (keyword matches)
- [ ] T041 [P] [US3] Add unit test for search across description (keyword matches)
- [ ] T042 [P] [US3] Add unit test for case-insensitive search (uppercase keyword finds match)
- [ ] T043 [P] [US3] Add unit test for empty search results (friendly message shown)
- [ ] T044 [US3] Add unit test for multiple tasks with matching keyword (all returned)
- [ ] T045 [P] [US3] Add integration test for search CLI command
- [ ] T046 [US3] Add integration test for --search argument in list-tasks command

**Tests**:
- Unit: `pytest tests/unit/ -k search`
- Integration: `pytest tests/integration/test_cli_commands.py::test_search`
- Verify FR-012, FR-013, FR-014 satisfied

---

## Phase 5: US4 - Task Filtering

**Goal**: Implement task filtering by status/priority/tag, multi-filter support, and display-only behavior per FR-015 through FR-019 and US4 acceptance scenarios.

**Independent Test**: Can apply single filters, combine multiple filters, verify original data preserved, test all filter types. Delivers focused viewing value once priority/tags exist.

- [ ] T047 [P] [US4] Add FilterCriteria dataclass to filter_service.py (completion_status, priority, tag)
- [ ] T048 [P] [US4] Implement filter_tasks() in filter_service.py (multi-filter intersection logic)
- [ ] T049 [P] [US4] Add "No tasks match these filters" message for zero filter results (from clarifications)
- [ ] T050 [P] [US4] Add --filter-status argument to list-tasks CLI command (complete/incomplete)
- [ ] T051 [P] [US4] Add --filter-priority argument to list-tasks CLI command (high/medium/low)
- [ ] T052 [P] [US4] Add --filter-tag argument to list-tasks CLI command (single tag)
- [ ] T053 [P] [US4] Add unit test for status filter (complete/incomplete)
- [ ] T054 [P] [US4] Add unit test for priority filter (high/medium/low)
- [ ] T055 [P] [US4] Add unit test for tag filter (single tag match)
- [ ] T056 [P] [US4] Add unit test for multi-filter intersection (status + priority)
- [ ] T057 [P] [US4] Add unit test for multi-filter intersection (status + priority + tag)
- [ ] T058 [P] [US4] Add unit test for zero filter results (message displayed)
- [ ] T059 [P] [US4] Add unit test for display-only behavior (original tasks unchanged)
- [ ] T060 [P] [US4] Add integration test for single status filter
- [ ] T061 [P] [US4] Add integration test for single priority filter
- [ ] T062 [P] [US4] Add integration test for single tag filter
- [ ] T063 [P] [US4] Add integration test for combined filters (status + priority)
- [ ] T064 [P] [US4] Add integration test for combined filters (all three)
- [ ] T065 [P] [US4] Add integration test for filter removal (list all tasks shown, data unchanged)

**Tests**:
- Unit: `pytest tests/unit/ -k filter`
- Integration: `pytest tests/integration/test_cli_commands.py::test_filter`
- Verify FR-015, FR-016, FR-017, FR-018, FR-019 satisfied

---

## Phase 6: US5 - Task Sorting

**Goal**: Implement task sorting (alphabetical, priority, due date), due date null handling, and display-only behavior per FR-020 through FR-024 and US5 acceptance scenarios.

**Independent Test**: Can apply each sort option, verify correct ordering, check due date null handling, confirm stored data unchanged. Delivers organized viewing value.

- [ ] T066 [P] [US5] Create SortOption enum (TITLE, PRIORITY, DUE_DATE)
- [ ] T067 [P] [US5] Implement sort_service.py
- [ ] T068 [P] [US5] Implement sort_tasks() in sort_service.py (alphabetical, priority, due date)
- [ ] T069 [P] [US5] Add priority order mapping to constants.py (HIGH=0, MEDIUM=1, LOW=2)
- [ ] T070 [P] [US5] Implement due date sort key (dates first, None values last)
- [ ] T071 [P] [US5] Add --sort-by argument to list-tasks CLI command (title/priority/due-date)
- [ ] T072 [P] [US5] Add unit test for alphabetical sort (case-insensitive)
- [ ] T073 [P] [US5] Add unit test for priority sort (HIGH > MEDIUM > LOW order)
- [ ] T074 [P] [US5] Add unit test for due date sort (dated first, None last)
- [ ] T075 [P] [US5] Add unit test for same-value sorting (all medium priority)
- [ ] T076 [P] [US5] Add unit test for display-only behavior (original tasks unchanged)
- [ ] T077 [P] [US5] Add integration test for title sort
- [ ] T078 [P] [US5] Add integration test for priority sort
- [ ] T079 [P] [US5] Add integration test for due date sort
- [ ] T080 [P] [US5] Add integration test for sort + filter combination (sorted filtered results)

**Tests**:
- Unit: `pytest tests/unit/ -k sort`
- Integration: `pytest tests/integration/test_cli_commands.py::test_sort`
- Verify FR-020, FR-021, FR-022, FR-023, FR-024 satisfied

---

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Ensure all features work together, verify backward compatibility, validate performance targets, add cross-feature test scenarios.

**Independent Test**: Can execute full workflow (create task with priority/tags, search, filter, sort), verify all Basic Level features operational, confirm performance <1 second for 1000 tasks.

- [ ] T081 Add unit test for combined search + filter
- [ ] T082 Add unit test for combined filter + sort
- [ ] T083 Add unit test for combined search + sort
- [ ] T084 Add unit test for combined search + filter + sort (full workflow)
- [ ] T085 Add integration test for full workflow (create with priority/tags, search, filter, sort)
- [ ] T086 Add contract test for SC-001 (priority assignment <10 seconds)
- [ ] T087 Add contract test for SC-003 (tag operations <15 seconds)
- [ ] T088 Add performance test for search (1000 tasks <1 second)
- [ ] T089 Add performance test for filter (1000 tasks <1 second)
- [ ] T090 Add performance test for sort (1000 tasks <1 second)
- [ ] T091 Run full test suite (pytest tests/)
- [ ] T092 Verify all Basic Level features operational (create/list/complete/delete tasks)
- [ ] T093 Verify SC-010 (priority and tags visible in all listings)
- [ ] T094 Manual testing of all CLI commands with new features
- [ ] T095 Verify backward compatibility (existing test suite passes)

**Tests**:
- Unit: `pytest tests/unit/ --cov=src --cov-report=html`
- Integration: `pytest tests/integration/`
- Contract: `pytest tests/contract/test_spec_compliance.py`

---

## MVP Scope

**Recommended Minimum Viable Product**: Complete Phase 1 (Setup) + Phase 2 (US1: Task Priority) + Phase 3 (US2: Task Tagging).

**Rationale**:
- US1 and US2 are P1/P2 priority stories providing core organization value
- Users can assign priority and categorize tasks independently
- Can be tested and validated as standalone increment
- Search/filter/sorting (US4/US5) are P3 - nice-to-have for usability

**Alternative MVP**: Phase 1 + Phase 2 (US1 only) if resources limited.

---

## Implementation Strategy

### Incremental Delivery

1. **MVP Sprint**: Phase 1, 2, 3 → Deliver priority + tagging features
2. **Usability Sprint**: Phase 4 (search) → Improve task finding
3. **Organization Sprint**: Phase 5 (filter) + Phase 6 (sort) → Complete feature set

### Parallel Opportunities

The following tasks can be executed in parallel as they touch different files with no dependencies:

| Task Group | Parallelizable Tasks |
|-------------|-------------------|
| US2 (Tagging) | T019, T020 [P] (CLI arguments), T021-T025 (display/utils) |
| US3 (Search) | T040-T043 (unit tests), T045, T046 (integration tests) |
| US5 (Sorting) | T072-T076 (unit tests), T077-T080 (integration tests) |

### Critical Path

Tasks that must complete in sequential order (no parallel execution):

```
T001-T006 (Setup) →
  T007-T018 (US1: Priority) → T085 (integration test) →
    T019-T034 (US2: Tagging) → T092 (integration test) →
      T035-T046 (US3: Search) → T045 (integration test) →
        T047-T065 (US4: Filter) → T080 (integration test) →
          T066-T080 (US5: Sort) → T084 (full workflow test) →
            T081-T095 (Polish)
```

---

## Completion Checklist

- [ ] All tasks completed (T001 through T095)
- [ ] All unit tests pass (pytest tests/unit/)
- [ ] All integration tests pass (pytest tests/integration/)
- [ ] All contract tests pass (pytest tests/contract/)
- [ ] Code coverage ≥ 80% (pytest-cov report)
- [ ] Performance targets met (search/filter/sort <1 second for 1000 tasks)
- [ ] Backward compatibility verified (Basic Level features operational)
- [ ] All functional requirements satisfied (FR-001 through FR-024)
- [ ] All success criteria met (SC-001 through SC-010)
- [ ] Manual CLI testing completed
- [ ] Documentation updated (quickstart.md reflects implementation)

---

## Notes

- **Constitution Compliance**: All tasks comply with Section I (Spec-Driven Development) and Section IV (Technology Constraints - Python 3.11+, in-memory)
- **Phase Governance**: All features within Phase I scope (in-memory CLI, no persistence)
- **Testing Strategy**: Unit tests per feature, integration tests for user stories, contract tests for spec compliance
- **Performance Budget**: <1 second for 1000 tasks operations (well within Python list comprehension performance)

**Total Tasks**: 95 (including unit, integration, contract, and polish tasks)

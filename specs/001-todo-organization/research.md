# Research: Todo Organization & Usability

**Feature**: 001-todo-organization | **Date**: 2025-12-31 | **Phase**: 0

## Overview

Research for extending Phase I In-Memory CLI Todo application with organization and usability features. All decisions comply with project constitution and Phase I constraints.

## Technical Decisions

### Decision 1: In-Memory Data Structure

**Decision**: Continue using Python dict/set-based in-memory storage, extend Task model with priority, tags, due_date attributes.

**Rationale**:
- Constitution Section III, Phase I definition explicitly requires "Pure Python, no persistence, CLI interface only"
- Existing architecture uses dict/set for state management (src/models/task.py)
- Extending existing model maintains backward compatibility (SC-009)
- No performance concern for 1000 tasks in-memory (SC-004, SC-005, SC-007 all specify <=1 second)

**Alternatives Considered**:
- SQLite with persistence: REJECTED - violates Phase I scope ("no persistence")
- External Redis cache: REJECTED - violates Phase I scope ("pure Python, no external databases")

---

### Decision 2: CLI Input Validation Approach

**Decision**: Use argparse validation with custom validators for priority values, tag string validation.

**Rationale**:
- Existing CLI uses argparse framework
- FR-003, FR-007 require validation with helpful error messages
- argparse integrates seamlessly with existing command structure
- Python 3.11+ has robust validation libraries (dataclass with __post_init__)

**Alternatives Considered**:
- Schema validation library (pydantic): REJECTED - additional dependency not required
- Custom exception-based validation: REJECTED - argparse provides better user experience

---

### Decision 3: Search & Filter Implementation Strategy

**Decision**: Implement search/filter as pure Python list comprehensions and filtering operations, no external libraries.

**Rationale**:
- Constitution Section I requires spec-driven development (no adding capabilities beyond spec)
- FR-012-018 specify exact behavior (title/description matching, case-insensitive, multi-filter)
- Python list comprehensions are O(n) which meets <1 second requirement for 1000 tasks
- Maintain consistency with existing in-memory architecture

**Alternatives Considered**:
- Regular expression library (re): REJECTED - overkill for simple substring matching
- Search library (whoosh, elasticlun): REJECTED - violates Phase I scope

---

### Decision 4: Sort Implementation Strategy

**Decision**: Use Python's sorted() with custom key functions for different sort options.

**Rationale**:
- FR-020-023 specify three sort types: alphabetical, priority, due date
- sorted() is O(n log n) for list operations, well within performance budget
- Custom key functions allow clear, testable sort logic
- Due date handling (nulls last) easily implemented with tuple keys

**Alternatives Considered**:
- Full sort library implementation: REJECTED - adds dependency, Python sorted() is sufficient

---

### Decision 5: Project Structure Approach

**Decision**: Extend existing structure, add new service modules for filter/sort separation.

**Rationale**:
- Constitution Section V requires clean architecture and separation of concerns
- Existing structure: src/models/, src/services/, src/cli/, tests/
- Adding filter_service.py and sort_service.py maintains separation
- Extending task.py in-place (not replacing) ensures backward compatibility

**Alternatives Considered**:
- Monolithic service file: REJECTED - violates separation of concerns
- Complete rewrite of model layer: REJECTED - risks breaking existing functionality

---

## Dependencies

**Python Standard Library**:
- `dataclasses`: Extended Task model with type hints
- `typing`: Type annotations for new attributes (priority, tags, due_date)
- `argparse`: Input validation framework
- `datetime`: Due date handling (FR-022)

**Existing Project Dependencies**:
- pytest: Testing framework (existing)
- pytest-cov: Coverage measurement (existing)

**New External Dependencies**: None required per Phase I constraints.

---

## Performance Analysis

### Search Complexity

- **Operation**: Case-insensitive substring match across title and description
- **Data Structure**: List of Task objects
- **Algorithm**: O(n * m) where n = tasks, m = query length
- **Worst Case (1000 tasks, 10-char query)**: ~10,000 operations
- **Python Execution Time**: <1ms (well within SC-004 requirement of 1 second)

### Filter Complexity

- **Operation**: Boolean filtering with multiple criteria
- **Data Structure**: List comprehension
- **Algorithm**: O(n) where n = tasks
- **Worst Case (1000 tasks)**: ~1,000 operations
- **Python Execution Time**: <1ms (well within SC-005 requirement of 1 second)

### Sort Complexity

- **Operation**: Timsort (Python's default)
- **Data Structure**: List of Task objects
- **Algorithm**: O(n log n) where n = tasks
- **Worst Case (1000 tasks)**: ~10,000 comparisons
- **Python Execution Time**: <1ms (well within SC-007 requirement of 1 second)

---

## Testing Strategy

### Unit Tests

- **test_task_model.py**: Task dataclass extensions, validation logic
- **test_filter_service.py**: Filter combinations, edge cases (zero results, empty tags)
- **test_sort_service.py**: Sort options, due date null handling, equal value sorting

### Integration Tests

- **test_cli_commands.py**: End-to-end command flows (create with priority, add tags, search, filter, sort)

### Contract Tests

- **test_spec_compliance.py**: Verify all FR-001 through FR-024 are satisfied

---

## Compliance Summary

| Constitution Section | Decision | Compliance |
|------------------|----------|------------|
| Spec-Driven Development | All features trace to FR-001 through FR-024 | PASS |
| Technology Constraints | Python 3.11+, in-memory, no persistence | PASS |
| Phase Governance | Phase I scope (in-memory CLI) | PASS |
| Architecture Principles | Clean separation (filter/sort services) | PASS |
| Security | Input validation, no secrets | PASS |
| Reliability | Restart-safe (in-memory) | PASS |

**Status**: READY FOR PHASE 1 DESIGN

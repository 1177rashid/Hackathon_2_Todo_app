# Research: Phase I In-Memory CLI Todo Application

**Branch**: `001-phase1-inmemory-cli`
**Date**: 2025-12-29
**Status**: Complete

---

## Research Summary

Phase I is intentionally simple with no external dependencies. All technical decisions
are predetermined by the constitution and specification. No research was required.

---

## Technical Decisions

### Decision 1: Implementation Language

**Decision**: Python (standard library only)

**Rationale**: Constitution mandates Python as the backend language for all phases.
Phase I specification explicitly excludes external dependencies.

**Alternatives Considered**: None - constitutionally mandated.

---

### Decision 2: Data Storage Approach

**Decision**: In-memory Python list with sequential integer ID generation

**Rationale**:
- Specification requires in-memory only (no persistence)
- Specification requires deterministic ordering (creation order)
- Specification requires stable, auto-generated unique IDs
- A Python list maintains insertion order (deterministic)
- Sequential integer IDs (starting from 1) satisfy uniqueness and stability requirements

**Alternatives Considered**:
- Dictionary with UUID keys: Rejected - UUIDs are less user-friendly for CLI input
- Set: Rejected - does not maintain insertion order

---

### Decision 3: CLI Framework

**Decision**: Python standard library only (input/print functions)

**Rationale**:
- Specification requires menu-based text CLI
- Specification excludes external dependencies
- Python's built-in `input()` and `print()` are sufficient for Phase I requirements

**Alternatives Considered**:
- argparse: Rejected - designed for command-line arguments, not interactive menus
- Third-party CLI libraries (click, rich, etc.): Rejected - violates no-dependencies constraint

---

### Decision 4: ID Generation Strategy

**Decision**: Sequential positive integers starting from 1, never reused within session

**Rationale**:
- Specification assumption #2: "Tasks are numbered with positive integers starting from 1"
- Specification FR-005: "Task IDs MUST remain stable for the duration of the program session"
- Simple counter increments on each task creation
- Deleted task IDs are NOT recycled (ensures stability)

**Alternatives Considered**:
- Reusing deleted IDs: Rejected - violates stability requirement
- Starting from 0: Rejected - specification explicitly states "starting from 1"

---

### Decision 5: Input Validation Approach

**Decision**: Validate at CLI boundary, domain entity enforces invariants

**Rationale**:
- FR-033: System MUST NOT crash on invalid input
- FR-034: System MUST display helpful error messages
- Clean Architecture principle: validation at boundaries
- Domain entity should enforce its own invariants (non-empty title)

**Alternatives Considered**:
- Validation only in CLI: Rejected - domain would accept invalid state
- Validation only in domain: Rejected - error messages would be less user-friendly

---

## Unknowns Resolved

| Unknown | Resolution | Source |
|---------|------------|--------|
| Python version | Python 3.x (any modern version) | Standard library only, no version-specific features |
| Menu format | Numbered options (1-7) | FR-026: "numbered menu of available operations" |
| Task display format | ID, title, description, status | FR-012 |
| Error message style | User-friendly text, no stack traces | FR-030 |

---

## Phase I Constraints Verification

| Constraint | Status | Notes |
|------------|--------|-------|
| No persistence | COMPLIANT | In-memory list only |
| No databases | COMPLIANT | No database usage |
| No files | COMPLIANT | No file I/O |
| No authentication | COMPLIANT | Single-user, no auth |
| No web/API/HTTP | COMPLIANT | CLI only |
| No background processes | COMPLIANT | Synchronous operation |
| No external dependencies | COMPLIANT | Standard library only |
| Pure Python | COMPLIANT | Python implementation |

---

## Conclusion

All technical decisions are straightforward given the Phase I constraints. No external
research or dependency evaluation was necessary. The implementation can proceed with:

1. Python standard library only
2. In-memory list for task storage
3. Sequential integer ID generation
4. Built-in input/print for CLI interaction
5. Boundary validation with domain invariant enforcement

# Spec Drift Detector

## Purpose

This skill detects and prevents divergence between specification and implementation. It acts as a vigilant observer that ensures every implementation change, behavior addition, or modification has a corresponding specification entry, maintaining strict spec-first discipline.

The skill is designed to:
- Identify features not defined in `/sp.specify`
- Block implementation if spec is outdated
- Require spec updates before behavior changes
- Maintain strict spec-first discipline
- Document drift detection and resolution

## When This Skill Must Be Applied

This skill MUST be invoked:

1. **Before any implementation begins** - Validate that proposed work is specified
2. **When new behaviors are proposed** - Check if spec exists for feature
3. **After code changes are made** - Verify implementation still matches spec
4. **During code review** - Confirm no unspecified behavior was introduced
5. **When behavior differs from expectations** - Determine if spec or implementation is wrong
6. **Before merging any PR** - Final drift gate check

This skill is triggered by:
- The `spec-driven-architect` agent during delegation
- Any agent before writing implementation code
- Manual invocation when compliance is in question
- CI/CD pipelines (if automated in later phases)

## Core Responsibilities

### 1. Specification Existence Check

The detector ensures a specification exists for all work:

**Existence Validation**:
```
1. Check if `specs/<feature>/spec.md` exists
2. Verify specification is not in "Draft" or "Needs Clarification" status
3. Confirm specification includes required sections:
   - User Scenarios & Testing
   - Functional Requirements
   - Success Criteria
4. Validate specification was created or updated recently
```

**Missing Specification Detection**:
```
Scenario: Request to implement "task search functionality"

Detector Check:
  - Does specification exist for task search?
    NO → STOP IMPLEMENTATION
  - Is search mentioned in any existing spec?
    NO → REQUIRE SPEC CREATION

Detector Response:
  "Cannot proceed with implementation. Feature 'task search'
   is not specified. Run /sp.specify to create specification first."
```

### 2. Behavior-Requirement Mapping

The detector maps implementation behaviors to specification requirements:

**Mapping Validation**:
```
For each behavior in implementation:

1. Identify behavior (e.g., "sort tasks by priority")
2. Locate corresponding requirement in spec (e.g., FR-012)
3. Verify behavior matches requirement exactly
4. Check if behavior is documented in acceptance scenarios

Result:
  ✓ Mapped → Behavior has specification backing
  ✗ Unmapped → Behavior requires specification
```

**Drift Detection Pattern**:
```
Pattern 1: Implementation has behavior not in spec
  Example: Code filters tasks by "completed" status
  Spec Check: FR-XYZ mentions filtering?
    NO → SPEC DRIFT DETECTED

Pattern 2: Spec requires behavior not implemented
  Example: FR-005 requires "sort by due date"
  Implementation Check: Sorting exists?
    NO → IMPLEMENTATION GAP DETECTED

Pattern 3: Behavior differs from spec
  Example: Spec says "show error message"
  Implementation: Shows "error code E001"
    NO → SPEC-IMPLEMENTATION MISMATCH DETECTED
```

### 3. Specification Currency Validation

The detector ensures specifications are up-to-date with current implementation:

**Currency Checks**:
```
Check 1: Specification Timestamp
  - When was spec last modified?
  - Has code been modified since then?
  - If code modified after spec → POTENTIAL DRIFT

Check 2: Acceptance Criteria Status
  - Are all acceptance criteria implemented?
  - Are there passing tests for each criterion?
  - If criteria unimplemented → SPEC NOT MET

Check 3: Edge Case Coverage
  - Does implementation handle edge cases not in spec?
  - Does spec document edge cases in implementation?
  - If mismatch → SPEC DRIFT
```

**Outdated Spec Detection**:
```
Scenario: Code handles "empty task list" scenario, but spec doesn't document it

Detector Check:
  - Does spec mention empty list handling?
    NO → SPEC DRIFT
  - Does implementation handle it?
    YES → DRIFT TYPE: Undocumented Behavior

Detector Response:
  "Specification drift detected. Implementation handles 'empty task list'
   scenario, but this is not documented in spec.

   Action Required:
   1. Update spec to document empty list handling
   2. OR remove behavior if it's outside scope
   Current Spec Status: OUTDATED"
```

### 4. Specification Update Enforcement

The detector enforces spec-first discipline by requiring updates:

**Update Requirements Matrix**:

| Change Type | Spec Update Required | Enforcement Level |
|-------------|---------------------|-------------------|
| Add new feature | YES (full spec) | BLOCKING |
| Modify existing behavior | YES (update relevant sections) | BLOCKING |
| Add edge case handling | YES (document in edge cases) | WARNING |
| Improve error messages | YES (update if spec messages) | ADVISORY |
| Refactor code only | NO (if behavior unchanged) | NONE |

**Enforcement Process**:
```
Step 1: Detect Drift
  → Identify where implementation differs from spec
Step 2: Classify Drift
  → BLOCKING, WARNING, or ADVISORY
Step 3: Require Action
  → BLOCKING: Must update spec before proceeding
  → WARNING: Should update spec, but may proceed
  → ADVISORY: Document for next spec revision
Step 4: Track Resolution
  → Mark as resolved when spec is updated
```

### 5. Drift Reporting and Tracking

The detector generates clear reports on spec-implementation alignment:

**Drift Report Template**:
```
SPEC DRIFT DETECTION REPORT
Timestamp: [ISO-8601]
Project: Evolution of Todo - Phase I
Feature: [feature name]

Alignment Status: [ALIGNED | DRIFT DETECTED | BLOCKED]

Drift Items Found: [count]

Drift Details:
---

[Item 1]
Type: [UNDOCUMENTED_BEHAVIOR | SPEC_GAP | MISMATCH | OUTDATED_SPEC]
Severity: [BLOCKING | WARNING | ADVISORY]

Specification Location:
  File: specs/<feature>/spec.md
  Section: [relevant section]

Implementation Location:
  File: [code file]
  Lines: [line numbers]

Description:
  [Clear description of drift]

Impact:
  [What this drift means for spec-driven development]

Required Action:
  - [ ] [Specific action to resolve drift]
  - [ ] [Additional actions]
Resolution Status: [PENDING | IN_PROGRESS | RESOLVED]

---

[Item 2]
[... repeat for each drift item ...]

Summary:
  - Total Drift Items: [count]
  - Blocking Items: [count]
  - Warning Items: [count]
  - Advisory Items: [count]

Recommendation:
  [BLOCK | PROCEED WITH CAUTION | PROCEED]
```

## Inputs & Outputs

### Inputs

| Input | Description | Example |
|--------|-------------|---------|
| `proposed_behavior` | New behavior to implement | `"sort tasks by priority descending"` |
| `implementation_code` | Existing code to validate | File paths, function names, code snippets |
| `spec_path` | Path to relevant specification | `specs/001-advanced-todo-features/spec.md` |
| `feature_name` | Feature being worked on | `"advanced-todo-features"` |
| `change_type` | Type of change being made | `"NEW_FEATURE"`, `"MODIFICATION"`, `"REFACTOR"` |

### Outputs

All outputs follow this structure:

```python
{
    "drift_status": "ALIGNED" | "DRIFT_DETECTED" | "BLOCKED",
    "drift_items": list[dict],  # List of drift details
    "blocking_count": int,
    "warning_count": int,
    "advisory_count": int,
    "recommendation": "BLOCK" | "PROCEED_WITH_CAUTION" | "PROCEED",
    "required_actions": list[str],
    "spec_status": "CURRENT" | "OUTDATED" | "MISSING"
}
```

## Decision Rules

### Rule 1: No Spec Exists

**Condition**: Feature or behavior has no specification
**Decision**: BLOCK
**Requirements**:
- Specification must be created via `/sp.specify`
- Spec must pass quality validation
- Spec must not be in Draft status

### Rule 2: Behavior Not in Spec

**Condition**: Implementation has behavior not documented in spec
**Decision**: BLOCK (for new behaviors) or WARNING (for edge cases)
**Requirements**:
- New features: Full spec required
- Edge cases: Document in spec edge cases section
- Error handling: Document in functional requirements

### Rule 3: Spec Gap in Implementation

**Condition**: Spec requires behavior not implemented
**Decision**: WARNING
**Requirements**:
- Implement missing behavior
- OR update spec to remove requirement
- Document decision rationale

### Rule 4: Behavior Mismatch

**Condition**: Implementation behavior differs from spec description
**Decision**: BLOCK
**Requirements**:
- Align implementation with spec
- OR update spec if change is intentional
- Re-validate after alignment

### Rule 5: Spec Outdated

**Condition**: Spec was modified before recent code changes
**Decision**: WARNING
**Requirements**:
- Review code changes for new behaviors
- Update spec if drift detected
- Document review findings

## Constraints

### Global Constraints

1. **Spec First**: All implementation work requires spec backing
2. **No Undocumented Behavior**: Every behavior has spec reference
3. **Alignment Required**: Implementation must match spec exactly
4. **Update Before Proceed**: Blocking drift resolved before work continues
5. **Document All Changes**: Spec reflects all implementation decisions

### Phase I Constraints

1. **Manual Detection**: Drift detection is manual (no automated analysis yet)
2. **Simple Spec Structure**: Specs follow template without complex versioning
3. **Human-In-The-Loop**: Detector provides findings, humans make decisions
4. **No CI Integration**: Drift checks are manual, not automated in pipelines
5. **Advisory for Refactors**: Code-only changes may proceed with documentation

## Failure Handling

### Failure Scenario 1: Missing Specification

**Input**: Request to implement "task tagging" without spec

**Detector Response**:
```
SPEC DRIFT DETECTOR: BLOCK

Proposed Feature: Task tagging functionality
Status: BLOCKED - Missing Specification

Drift Type: MISSING_SPECIFICATION
Severity: BLOCKING

Reason:
  Feature "task tagging" has no specification.
  Cannot proceed with implementation.

Required Actions:
  1. Run /sp.specify to create specification for task tagging
  2. Ensure spec includes:
     - User scenarios
     - Functional requirements
     - Success criteria
  3. Re-submit implementation request after spec exists

Alignment Status: BLOCKED
Recommendation: CREATE SPECIFICATION FIRST
```

### Failure Scenario 2: Undocumented Behavior

**Input**: Code filters by "completed" status but spec doesn't mention filtering

**Detector Response**:
```
SPEC DRIFT DETECTOR: DRIFT_DETECTED

Feature: Basic todo features
Status: DRIFT DETECTED - Undocumented Behavior

Drift Type: UNDOCUMENTED_BEHAVIOR
Severity: WARNING

Specification Location:
  File: specs/001-todo-organization/spec.md
  Section: Functional Requirements
  Requirement: FR-XYZ (task filtering)

Implementation Location:
  File: src/state/task_store.py
  Function: get_filtered_tasks()

Description:
  Implementation filters tasks by completion status,
  but specification does not document filtering behavior.

Impact:
  Medium risk - behavior exists without spec backing.
  Tests may fail if they expect spec-only features.

Required Actions:
  1. Update spec to document task filtering:
     - Add FR for "filter by status" functionality
     - Document available filter values (completed, incomplete, all)
     - Add acceptance scenarios for filtering
  2. OR remove filtering if it's outside intended scope
  3. Re-run spec quality validation

Resolution Status: PENDING SPEC UPDATE
Alignment Status: DRIFT_DETECTED (1 Warning)
Recommendation: UPDATE SPECIFICATION
```

### Failure Scenario 3: Spec-Implementation Mismatch

**Input**: Spec requires error message "Error [E003]: Task not found" but code shows different text

**Detector Response**:
```
SPEC DRIFT DETECTOR: BLOCK

Feature: Basic todo features
Status: BLOCKED - Behavior Mismatch

Drift Type: MISMATCH
Severity: BLOCKING

Specification Location:
  File: specs/001-todo-organization/spec.md
  Section: Error Scenarios and Handling
  Spec Requirement: "Error [E003]: Task not found"

Implementation Location:
  File: src/cli/handlers.py
  Function: handle_delete()
  Lines: 78-82

Description:
  Specification requires error message: "Error [E003]: Task not found"
  Implementation displays: "Error: Task ID does not exist"

  Mismatch: Error message text differs from specification.

Impact:
  Medium risk - User-facing messages differ from documented behavior.
  Test failures likely if tests check exact message text.

Required Actions:
  1. Determine correct message:
     - Option A: Update implementation to match spec
     - Option B: Update spec to match implementation (if change was intentional)
  2. If Option A (fix implementation):
     - Change message to: "Error [E003]: Task not found"
  3. If Option B (update spec):
     - Update spec.md line to: "Error [E003]: Task ID does not exist"
     - Update acceptance scenarios accordingly
     - Update all related documentation

Resolution Status: PENDING DECISION
Alignment Status: BLOCKED
Recommendation: RESOLVE MISMATCH BEFORE PROCEEDING
```

### Failure Scenario 4: Specification is Outdated

**Input**: Code was modified 3 days ago, spec was modified 2 weeks ago

**Detector Response**:
```
SPEC DRIFT DETECTOR: DRIFT_DETECTED

Feature: Advanced todo features
Status: DRIFT DETECTED - Outdated Specification

Drift Type: OUTDATED_SPEC
Severity: WARNING

Timestamp Comparison:
  Specification Last Modified: 2025-12-15
  Code Last Modified: 2025-12-28

Description:
  Code has been modified more recently than specification.
  This indicates potential drift where implementation evolved
  beyond what specification defines.

Impact:
  Medium risk - specification may no longer accurately reflect implementation.

Required Actions:
  1. Review code changes since spec was last modified
  2. Identify any new behaviors or modifications
  3. Update specification to document changes:
     - Add new FR numbers for new behaviors
     - Update acceptance scenarios
     - Add new edge cases if applicable
  4. Re-run spec quality validation

Review Focus Areas:
  - src/domain/task.py (new fields added?)
  - src/cli/handlers.py (new command handlers?)
  - src/state/task_store.py (new operations?)

Resolution Status: PENDING REVIEW
Alignment Status: DRIFT_DETECTED (1 Warning)
Recommendation: REVIEW AND UPDATE SPECIFICATION
```

### Failure Scenario 5: Spec Gaps Detected

**Input**: Spec requires FR-015 "sort by due date" but implementation doesn't include sorting

**Detector Response**:
```
SPEC DRIFT DETECTOR: DRIFT_DETECTED

Feature: Advanced todo features
Status: DRIFT_DETECTED - Implementation Gap

Drift Type: SPEC_GAP
Severity: WARNING

Specification Location:
  File: specs/001-advanced-todo-features/spec.md
  Section: Functional Requirements
  Requirement: FR-015 "System MUST allow users to view tasks sorted by due date"

Implementation Check:
  File: src/state/task_store.py
  Function: get_sorted_tasks()
  Result: NOT FOUND

Description:
  Specification FR-015 requires sorting functionality, but
  implementation does not include sorting by due date.

Impact:
  Medium risk - feature is documented but not implemented.
  Acceptance criteria SC-005 cannot be met.

Required Actions:
  1. Implement sorting functionality:
     - Add sort_by_due_date() method to task_store
     - Add CLI command option for sorting
     - Update display to show sorted results
  2. OR update specification if sorting is not actually needed:
     - Remove FR-015 from requirements
     - Remove SC-005 from success criteria
     - Update plan.md to reflect reduced scope

Resolution Status: PENDING DECISION
Alignment Status: DRIFT_DETECTED (1 Warning)
Recommendation: IMPLEMENT OR UPDATE SPECIFICATION
```

## Reusability Notes

### Cross-Phase Application

This skill is designed for reuse across all project phases:

- **Phase I**: Manual drift detection, simple spec structures
- **Phase II**: Will integrate with automated testing for spec coverage
- **Phase III**: Will add API contract drift detection
- **Phase IV+**: Will adapt to distributed spec management, versioning

The skill does NOT hardcode Phase I rules. Instead it:
1. Applies spec-first principles universally
2. Adapts to spec complexity as project grows
3. Maintains same detection patterns across phases

### Extension Points

For future phases, detector can be extended with:
- Automated diff tools (git-based spec tracking)
- Test coverage analysis (which specs have tests)
- API contract validation (OpenAPI vs implementation)
- Continuous spec validation (CI/CD integration)
- Spec versioning and migration tracking

## Conceptual Example

**Scenario**: Developer proposes adding "task export to JSON" feature

**Detector Evaluation Process**:

1. **Specification Check**:
   ```
   Does spec mention "export" or "JSON"?
   - Scan specs/001-todo-organization/spec.md
   - Scan specs/001-advanced-todo-features/spec.md
   Result: NO MENTION FOUND
   ```

2. **Phase Scope Check**:
   ```
   Is "export" in Phase I scope?
   - Review constitution Phase I constraints
   - Constitution says: "In-memory only, no file I/O"

   Result: EXPORT IS OUT OF SCOPE
   ```

3. **Drift Classification**:
   ```
   Type: MISSING_SPECIFICATION
   Severity: BLOCKING (also Phase I violation)
   This is both a spec gap AND a scope violation.
   ```

**Detector Response**:
```
SPEC DRIFT DETECTOR: BLOCK

Proposed Feature: Task export to JSON
Status: BLOCKED - Missing Specification AND Out of Scope

Drift Type: MISSING_SPECIFICATION
Severity: BLOCKING

Phase I Scope Violation:
  Category: Persistence Violation
  Constitution: .specify/memory/constitution.md
  Constraint: "In-memory data only (no persistence)"

Reason:
  1. Feature "task export to JSON" has no specification
  2. Export functionality violates Phase I constraints (no file I/O)

Required Actions:
  Option 1 - Defer to Future Phase:
     - Document export feature for Phase II consideration
     - Create ADR if architecturally significant
  Option 2 - Reconsider Scope:
     - Run /sp.specify if this is truly needed in Phase I
     - Update constitution to allow file I/O (requires approval)
  Option 3 - Abandon:
     - Do not implement export functionality
     - Focus on Phase I in-memory features only

Alignment Status: BLOCKED (2 violations)
Recommendation: DO NOT PROCEED - Feature is out of Phase I scope
```

**Outcome**: Implementation blocked, directed toward appropriate phase or spec creation.

## Integration with Other Agents/Skills

### With spec-driven-architect
- Architect invokes detector before delegating any work
- Detector provides drift status to architect
- Architect makes decision based on detector's recommendation

### With spec-compliance-validator
- Validator checks compliance after implementation
- Detector checks compliance before implementation
- Coordination: Detector prevents drift, Validator confirms compliance

### With phase-scope-guard
- Detector checks spec existence, guard checks phase compliance
- Both must approve for implementation to proceed
- Coordination: Detector ensures spec exists, guard ensures scope compliance

### With task-model-evolution-guard
- Detector validates feature is specified before model changes
- Guard validates model changes are safe after spec exists
- Coordination: Detector ensures spec backing, guard ensures safe evolution

## Guiding Principle

> "Specifications are single source of truth. When implementation drifts from specification, we don't adjust to code—we adjust to specification first. The detector is vigilant observer that ensures every line of code has a corresponding specification, every behavior has documented requirements, and no feature creeps in without proper definition."

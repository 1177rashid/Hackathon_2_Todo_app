# Spec Compliance Validator

## Purpose

This skill enforces strict compliance between all implementation work and the authoritative project specifications. It acts as a validation checkpoint that ensures every code change, feature addition, or behavioral modification adheres exactly to what is defined in the constitution and feature specs.

The skill is designed to:
- Prevent specification drift during implementation
- Catch unspecified behavior before it enters the codebase
- Maintain the integrity of the spec-driven development methodology
- Ensure specs remain the single source of truth

## When This Skill Must Be Applied

This skill MUST be invoked:

1. **Before any implementation begins** - Validate the proposed work matches spec requirements
2. **After code changes are made** - Verify the implementation matches spec exactly
3. **During code review** - Confirm no unspecified behavior was introduced
4. **When behavior differs from expectations** - Determine if spec or implementation is wrong
5. **Before merging any PR** - Final compliance gate check

This skill SHOULD be triggered by:
- The `spec-driven-architect` agent during delegation
- Any agent before writing implementation code
- Manual invocation when compliance is in question

## Authoritative Documents

The validator uses these documents as sources of truth (in order of precedence):

1. **Constitution**: `.specify/memory/constitution.md`
   - Defines immutable project principles
   - Sets phase constraints and boundaries
   - Establishes quality standards and governance

2. **Feature Specs**: `specs/<feature>/spec.md`
   - Defines feature requirements and acceptance criteria
   - Specifies expected behavior and edge cases
   - Documents constraints and dependencies

## Validation Checklist

### Pre-Implementation Validation

Before any code is written, verify:

- [ ] The feature/behavior is explicitly defined in a spec
- [ ] The spec location is identified: `specs/<feature>/spec.md`
- [ ] All acceptance criteria are documented and testable
- [ ] The implementation approach does not violate constitution principles
- [ ] The work falls within current phase constraints
- [ ] No assumptions are being made about unspecified behavior

### Implementation Compliance Validation

For every code change, verify:

- [ ] **Behavior Match**: Code behavior matches spec description exactly
- [ ] **No Additions**: No behavior exists that is not specified
- [ ] **No Omissions**: All specified behavior is implemented
- [ ] **Acceptance Criteria**: All spec acceptance criteria are met
- [ ] **Constraints Respected**: Phase constraints are not violated
- [ ] **Constitution Alignment**: Code follows constitution principles

### Specific Violation Checks

#### Addition Violations (MUST REJECT)
- Adding features not in specs
- Implementing "nice to have" enhancements
- Adding error handling for unspecified edge cases
- Creating abstractions not required by specs
- Adding configuration options not specified

#### Removal Violations (MUST REJECT)
- Omitting specified behavior
- Skipping required validation
- Removing specified error handling
- Ignoring documented edge cases
- Failing to implement acceptance criteria

#### Modification Violations (MUST REJECT)
- Changing acceptance criteria during implementation
- Altering specified behavior to "fix" perceived issues
- Modifying error messages from spec
- Changing data formats without spec update
- Adjusting constraints without spec approval

## Rejection Behavior

When a violation is detected, the validator MUST:

### 1. Halt Implementation

Do NOT proceed with any code changes that violate specifications.

### 2. Identify the Violation

Provide clear documentation:

```
SPEC COMPLIANCE VIOLATION DETECTED

Violation Type: [Addition | Removal | Modification]
Severity: BLOCKING

Spec Reference: specs/<feature>/spec.md
Section: [specific section]

Expected (per spec):
  [quote from specification]

Actual/Proposed:
  [description of violating change]

Discrepancy:
  [clear explanation of the difference]
```

### 3. Request Spec Refinement

Direct the workflow toward spec modification, NOT code modification:

```
REQUIRED ACTION: Spec Refinement

The implementation cannot proceed because it would deviate from
the specification. The spec is the source of truth.

Options:
1. Modify the spec to include the desired behavior
   → Update: specs/<feature>/spec.md
   → Then: Re-run implementation

2. Abandon the change and implement as specified
   → The current spec will be implemented exactly

3. Clarify the spec if ambiguous
   → Add detail to: specs/<feature>/spec.md
   → Then: Re-validate and implement

DO NOT modify implementation to work around spec limitations.
The spec must be updated first.
```

### 4. Block Until Resolved

The validator maintains a blocking state until:
- The spec is updated to include the behavior, OR
- The violating change is abandoned, OR
- Ambiguity is clarified and implementation matches clarified spec

## Integration with Agents

### With spec-driven-architect

The `spec-driven-architect` agent should invoke this skill:
- Before delegating any implementation work
- When validating completed implementations
- When arbitrating spec vs. implementation disputes

### With task-domain-enforcer

Apply this skill to validate:
- Task entity properties match spec
- Domain invariants are as specified
- No additional domain logic is added

### With in-memory-state-manager

Apply this skill to validate:
- CRUD operations match spec exactly
- State management follows spec constraints
- No persistence behavior is added

### With cli-interface

Apply this skill to validate:
- Menu options match spec
- Input/output formats follow spec
- Error messages are as specified

## Phase-Agnostic Design

This skill is designed to work across all project phases:

- **Phase I**: Validates against Phase I constraints
- **Phase II+**: Will validate against updated constitution and expanded specs

The skill does not hardcode phase-specific rules. Instead, it:
1. Reads current constraints from constitution
2. Applies whatever constraints are defined
3. Adapts to spec evolution over time

## Validation Report Template

After validation, produce a report:

```
SPEC COMPLIANCE VALIDATION REPORT

Status: [PASSED | FAILED | BLOCKED]
Timestamp: [ISO-8601 datetime]

Documents Validated Against:
- Constitution: .specify/memory/constitution.md
- Feature Spec: specs/<feature>/spec.md

Checklist Results:
- [ ] Feature is specified: [PASS/FAIL]
- [ ] No additions detected: [PASS/FAIL]
- [ ] No omissions detected: [PASS/FAIL]
- [ ] No modifications detected: [PASS/FAIL]
- [ ] Acceptance criteria met: [PASS/FAIL]
- [ ] Phase constraints respected: [PASS/FAIL]
- [ ] Constitution principles followed: [PASS/FAIL]

Violations Found: [count]
[List of violations if any]

Recommendation:
[PROCEED WITH IMPLEMENTATION | HALT AND REFINE SPEC | CLARIFICATION NEEDED]
```

## Invocation

This skill can be invoked:

1. **Automatically** - By agents following spec-driven methodology
2. **Manually** - When compliance verification is needed
3. **As a gate** - Before code merges or deployments

## Guiding Principle

> "The spec defines what we build. The constitution defines how we build it.
> When implementation diverges from spec, we fix the spec—not the code.
> The validator is the guardian of this truth."

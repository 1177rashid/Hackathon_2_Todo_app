# Task Model Evolution Guard

## Purpose

This skill governs safe evolution of the Task data model across all project phases. It ensures that changes to task structure maintain backward compatibility, follow defined patterns, and prevent schema-breaking mutations that would compromise data integrity or require migration.

The skill is designed to:
- Define rules for adding new task fields and properties
- Enforce backward compatibility across feature tiers
- Require defaults for new optional attributes
- Prevent breaking schema changes without explicit approval
- Document model evolution rationale and impact

## When This Skill Must Be Applied

This skill MUST be invoked:

1. **Before adding new task properties** - Validate that new fields are appropriate and safe
2. **When modifying existing field types** - Ensure change is backward compatible
3. **When removing task attributes** - Validate no dependencies exist
4. **During schema design discussions** - Provide evolution guidance
5. **Before implementing new feature tiers** - Ensure model supports feature without breaking changes

This skill is triggered by:
- `task-domain-enforcer` agent when defining task entities
- `in-memory-state-manager` when designing data structures
- `spec-driven-architect` when evaluating data modeling decisions
- Manual invocation during architecture reviews

## Core Responsibilities

### 1. Field Addition Rules

When new properties are proposed for the Task model:

**Requirements:**
- MUST be optional (nullable) if not present in Basic features
- MUST define a sensible default value
- MUST NOT break existing task creation flows
- MUST NOT require data migration from Basic to Intermediate/Advanced

**Validation Checklist:**
- [ ] Field has a clear, descriptive name following existing naming conventions
- [ ] Type is compatible with Python standard library types
- [ ] Default value is explicitly defined and reasonable
- [ ] Field is documented with purpose and allowed values
- [ ] No existing code assumes this field is present

### 2. Backward Compatibility Enforcement

The guard enforces strict backward compatibility:

**Permitted Changes:**
- Adding optional fields with defaults
- Expanding allowed value ranges for existing fields (e.g., status enum)
- Adding helper methods that don't modify core structure
- Deprecating fields (with documentation) while maintaining support

**Prohibited Changes (without explicit spec):**
- Changing field types (e.g., str → int)
- Making required fields optional
- Removing fields without migration path
- Changing field semantics without spec update

**Compatibility Matrix:**

| Change Type | Basic → Intermediate | Basic → Advanced | Intermediate → Advanced |
|------------|---------------------|-------------------|-------------------------|
| Add optional field | ✅ Safe | ✅ Safe | ✅ Safe |
| Make field required | ❌ Breaking | ❌ Breaking | ❌ Breaking |
| Change field type | ❌ Breaking | ❌ Breaking | ❌ Breaking |
| Remove field | ❌ Breaking | ❌ Breaking | ❌ Breaking |

### 3. Default Value Requirements

All optional task fields MUST provide:

**Default Value Template:**
```
Field Name: [property_name]
Type: [Python type]
Default: [explicit default value]
Rationale: [why this default makes sense]
```

**Acceptable Default Values:**
- None / null (for truly optional data)
- Empty collection: [] (for lists), {} (for dicts)
- Zero or false (for numeric/boolean fields)
- Empty string: "" (for text fields)
- Current date/time (for timestamps)

**Unacceptable Defaults:**
- Magic numbers or arbitrary values without rationale
- Defaults that create side effects or state changes
- Defaults requiring external dependencies
- Defaults that mask validation errors

### 4. Schema Breaking Change Detection

The guard identifies breaking changes through:

**Pattern Matching:**
- Type modifications in class definitions
- Required field additions in data models
- Removal of previously available properties
- Changes to immutable field contracts

**Detection Algorithm:**
1. Compare current model schema against previous version
2. Identify structural differences (additions, removals, type changes)
3. Classify each change as: SAFE | COMPATIBLE | BREAKING
4. Generate impact report for BREAKING changes

**Impact Report Template:**
```
SCHEMA BREAKING CHANGE DETECTED

Change: [description of modification]
Impact: [which feature tiers affected]
Breaking Behavior: [specific breaking scenario]
Migration Path: [recommended approach if change is necessary]
Guard Recommendation: [APPROVE WITH MITIGATION | REJECT | DEFER TO NEXT PHASE]
```

### 5. Feature Tier Evolution Rules

The Task model evolves through feature tiers:

**Basic Tier (Phase I - Core)**
- Required fields: id, title, status
- Optional fields: description
- Invariants: id is immutable, status is enum (pending/in-progress/completed/cancelled)

**Intermediate Tier (Phase I - Extended)**
- Adds to Basic: priority, tags
- Invariants: priority is enum (low/medium/high), tags is list of strings
- Compatibility: Basic tasks remain valid (new fields default to None)

**Advanced Tier (Phase I - Intelligent)**
- Adds to Intermediate: due_date, recurrence_pattern
- Invariants: due_date is datetime (optional), recurrence_pattern is object (optional)
- Compatibility: Intermediate tasks remain valid (new fields default to None)

**Evolution Principles:**
- Each tier is a strict superset of previous tier
- No tier removes capabilities from previous tier
- Defaults ensure lower-tier tasks remain valid in higher-tier systems
- Feature flagging or optional enablement preferred over breaking changes

## Inputs & Outputs

### Inputs

| Input | Description | Example |
|--------|-------------|---------|
| `proposed_change` | Description of model modification | "Add 'due_date' field to Task" |
| `current_schema` | Existing Task model definition | Python class definition or dict |
| `previous_schema` | Task model before change | Python class definition or dict (optional) |
| `target_tier` | Feature tier being implemented | "Basic", "Intermediate", "Advanced" |
| `spec_reference` | Link to spec requiring change | `specs/001-advanced-todo-features/spec.md` |

### Outputs

All outputs follow this structure:

```python
{
    "validation_result": "APPROVED" | "CONDITIONAL" | "REJECTED",
    "change_type": "SAFE_ADDITION" | "COMPATIBLE" | "BREAKING",
    "default_value": any | None,
    "impact_summary": str,
    "requirements": list[str],
    "mitigation_suggestions": list[str] | None,
    "tier_compatibility": str  # e.g., "Basic → Intermediate: SAFE"
}
```

## Decision Rules

### Rule 1: Optional Field Addition

**Condition**: New field is optional and has sensible default
**Decision**: APPROVED
**Requirements**:
- Field name follows snake_case convention
- Type is standard library compatible
- Default is explicit and reasonable
- Field is documented

### Rule 2: Required Field Addition

**Condition**: New field is required for operation
**Decision**: REJECTED (with mitigation)
**Requirements**:
- Specification explicitly requires this field
- Migration path exists for existing data
- All task creation paths are updated
- Backward compatibility is addressed (e.g., two-phase rollout)

**Mitigation**: Make field optional first, then mark required in next phase after data migration

### Rule 3: Field Type Change

**Condition**: Changing type of existing field
**Decision**: REJECTED (with rare exceptions)
**Exceptions**:
- Type change is strictly additive (e.g., str → Union[str, None])
- All existing data conforms to new type
- Specification requires and documents change

**Mitigation**: Create new field with different name, deprecate old field

### Rule 4: Field Removal

**Condition**: Removing existing task property
**Decision**: REJECTED
**Requirements**:
- Field is no longer referenced in any spec
- Field is not used by any existing feature
- Removal is documented in ADR

**Mitigation**: Mark field as deprecated, remove in next major phase

### Rule 5: Recurrence Pattern Addition

**Condition**: Adding recurrence pattern field (Advanced tier)
**Decision**: CONDITIONAL
**Requirements**:
- Field is optional (defaults to None)
- No existing tasks are forced into recurrence
- Recurrence logic is external to Task model
- Validation rules are defined separately

**Approval**: APPROVED if recurrence_policy_engine skill validates

## Constraints

### Global Constraints

1. **No Breaking Changes Without Spec**: Schema-breaking changes require explicit spec updates
2. **Default Values Required**: All optional fields must have defined defaults
3. **Tier Compatibility**: Higher tiers must remain compatible with lower tiers
4. **Type Safety**: All types must be runtime-checkable and enforceable
5. **Documentation**: Every field must have purpose and allowed values documented

### Phase I Constraints

1. **Standard Library Only**: No third-party types or dependencies
2. **Simple Types**: Use built-in Python types (str, int, bool, list, dict, datetime)
3. **No Circular Dependencies**: Task model must not reference itself recursively
4. **Immutable IDs**: Task ID must never change after creation
5. **Status Enum**: Task status must be constrained to defined enum values

## Failure Handling

### Failure Scenario 1: Attempting to Add Required Field

**Input**: "Add 'due_date' as required field to Task model"

**Guard Response**:
```
MODEL EVOLUTION GUARD: REJECTED

Proposed Change: Add required field 'due_date' to Task model
Violation Type: Breaking Change

Reason:
  Adding a required field breaks backward compatibility with existing
  Basic and Intermediate tier tasks that don't have due dates.

Guard Recommendation: CONDITIONAL APPROVAL

Requirements for Approval:
1. Make 'due_date' optional with default None
2. Update all task creation paths to handle None case
3. Document that due_date becomes required in Phase II

Alternative:
  Defer required due_date to Phase II when migration infrastructure exists
```

### Failure Scenario 2: Changing Field Type

**Input**: "Change status field from str to Enum"

**Guard Response**:
```
MODEL EVOLUTION GUARD: REJECTED

Proposed Change: Change Task.status from str to Enum type
Violation Type: Type Modification Breaking Change

Reason:
  Type changes break serialization, comparison, and existing code assumptions.
  This would require migration of all in-memory task instances.

Guard Recommendation: REJECT WITH MITIGATION

Recommended Approach:
1. Keep status as str for Phase I
2. Document allowed values in specification
3. Phase II can introduce Enum with migration path
4. Create ADR if this is architecturally significant

Alternative:
  Use Union[str, Enum] if Python 3.10+ typing is available
```

### Failure Scenario 3: Adding Field Without Default

**Input**: "Add 'recurrence_pattern' field to Task"

**Guard Response**:
```
MODEL EVOLUTION GUARD: CONDITIONAL

Proposed Change: Add optional field 'recurrence_pattern' to Task
Violation Type: Missing Default Value

Reason:
  Field must define a default value to maintain backward compatibility.
  Existing tasks created before this change should not crash.

Guard Recommendation: APPROVE WITH CORRECTION

Required Corrections:
1. Define default value for 'recurrence_pattern': None
2. Document that None means "no recurrence"
3. Ensure all task operations handle None case correctly

Approval Status: PENDING DEFAULT VALUE DEFINITION
```

### Failure Scenario 4: Removing Existing Field

**Input**: "Remove 'description' field from Task model"

**Guard Response**:
```
MODEL EVOLUTION GUARD: REJECTED

Proposed Change: Remove 'description' field from Task model
Violation Type: Schema Breaking Change

Reason:
  Removing fields breaks data integrity and existing task instances.
  Users with tasks containing descriptions would lose data.

Guard Recommendation: REJECT

Requirements for Removal:
1. Field is not referenced in any active specification
2. No existing task instances use this field
3. Removal is documented in ADR with rationale
4. Migration or data preservation path exists

Alternative:
  Mark 'description' as deprecated in documentation
  Remove in Phase II with explicit data handling
```

## Reusability Notes

### Cross-Phase Application

This skill is designed for reuse across all project phases:

- **Phase I**: Enforces in-memory model constraints, CLI-appropriate types
- **Phase II**: Will validate persistence-ready model (database schemas)
- **Phase III**: Will enforce API-compatible model (JSON serialization)
- **Phase IV+**: Will adapt to multi-user, distributed models

The skill does NOT hardcode Phase I rules. Instead it:
1. Reads constraints from constitution
2. Applies whatever model evolution rules are defined
3. Adapts to tier expansion over time

### Extension Points

For future phases, the guard can be extended with:
- Database schema validation (foreign keys, indexes)
- API contract validation (JSON schema compatibility)
- Migration script generation for breaking changes
- Versioning strategy for model evolution

## Conceptual Example

**Scenario**: Intermediate tier adds priority to Task model

**Proposed Change**:
```
Add 'priority' field to Task model
- Type: str (enum: low, medium, high)
- Optional: Yes
- Default: "medium"
```

**Guard Evaluation**:

1. **Field Addition Check**: ✅ Field is optional
2. **Default Value Check**: ✅ Default "medium" is sensible
3. **Type Check**: ✅ str is standard library type
4. **Tier Compatibility**: ✅ Basic tasks remain valid (priority defaults to None in Basic tier)
5. **Backward Compatibility**: ✅ No existing code assumes priority exists

**Guard Response**:
```
MODEL EVOLUTION GUARD: APPROVED

Change Type: SAFE_ADDITION
Validation Result: APPROVED

Tier Compatibility: Basic → Intermediate: SAFE
  Basic tasks will have priority=None (default behavior)

Requirements:
1. Implement priority field with default None
2. Add validation for enum values (low, medium, high)
3. Update task display to handle None case
4. Document priority in feature spec

No breaking changes detected.
This evolution is safe for immediate implementation.
```

**Outcome**: Priority field is added safely, Basic tier continues to work, Intermediate tier gets enhanced functionality.

## Integration with Other Agents/Skills

### With task-domain-enforcer

- This guard validates model structure before domain enforcer implements invariants
- Domain enforcer enforces business rules on top of validated model
- Coordination: Guard defines WHAT exists, enforcer defines HOW it behaves

### With in-memory-state-manager

- Guard validates model before state manager implements data structures
- State manager follows model structure for serialization
- Coordination: Guard defines schema, state manager implements CRUD

### With recurrence_policy_engine

- When adding recurrence fields, guard delegates validation to recurrence policy
- Recurrence policy defines allowed patterns, guard ensures safe addition
- Coordination: Guard validates field addition, policy validates field values

### With spec-driven-architect

- Architect invokes guard when evaluating data modeling decisions
- Guard provides compatibility assessment for architectural proposals
- Coordination: Guard ensures evolution safety, architect makes final decision

## Guiding Principle

> "The Task model is the foundation. Evolution must be intentional, documented, and safe. Never break what exists—extend it thoughtfully, preserve compatibility, and maintain the trust of data that has been created."

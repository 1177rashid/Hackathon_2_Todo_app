---
id: 001
title: Evolution of Todo Constitution Creation
stage: constitution
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: system
command: /sp.constitution
labels: ["constitution", "governance", "spec-driven-development", "evolution-of-todo"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document, no code tests)
---

## Prompt

Create a SINGLE, GLOBAL CONSTITUTION for the entire software system named:

"Evolution of Todo"

This constitution applies to ALL phases of the project:
- Phase I: In-Memory Python CLI
- Phase II: Full-Stack Web Application
- Phase III: AI-Powered Conversational System
- Phase IV: Kubernetes-Based Local Deployment
- Phase V: Cloud-Native, Event-Driven Distributed System

The output MUST be a single Markdown file located at:
  /sp.constitution.md

────────────────────────────────────────
AUTHORITY & SUPREMACY
────────────────────────────────────────

This constitution is the SUPREME GOVERNING DOCUMENT.

- It overrides all specifications, plans, tasks, code, and agent instructions.
- If any conflict exists:
  Constitution → Specs → Plans → Tasks → Code
- Any violation of this constitution invalidates the work.

────────────────────────────────────────
1. SPEC-DRIVEN DEVELOPMENT (MANDATORY)
────────────────────────────────────────

The system MUST strictly enforce Spec-Driven Development.

Rules:
- No agent may write, generate, modify, or refactor code without approved specifications.
- All work MUST follow this immutable chain:

  Constitution → Specifications → Plans → Tasks → Implementation

- Code MUST be treated as a generated artifact, never as a source of truth.
- Behavioral changes MUST occur only by refining specifications, never by editing code directly.
- Any implementation without an explicit governing spec is invalid.

────────────────────────────────────────
2. AGENT BEHAVIOR & EXECUTION RULES
────────────────────────────────────────

All AI agents (including coding agents) MUST follow these rules:

- Humans MUST NOT write or modify source code manually.
- Agents MUST NOT invent features, APIs, fields, flows, or behaviors.
- Agents MUST NOT deviate from approved specifications or plans.
- Agents MUST NOT "fill gaps" using assumptions.
- If ambiguity is detected, agents MUST request spec clarification.
- Refinement MUST always happen at the specification or plan level, never in code.

Agents exist to EXECUTE intent, not to DEFINE intent.

────────────────────────────────────────
3. PHASE GOVERNANCE & EVOLUTION CONTROL
────────────────────────────────────────

- Each phase is strictly scoped by its approved specifications.
- Features, patterns, infrastructure, or assumptions from future phases
  MUST NOT leak into earlier phases.
- Backward compatibility MUST be preserved across phases unless explicitly revised by spec.
- Architectural evolution is allowed ONLY through updated specifications and plans.
- Phases MUST be completed sequentially; skipping or merging phases is prohibited.

────────────────────────────────────────
4. TECHNOLOGY & PLATFORM CONSTRAINTS
────────────────────────────────────────

The following technology constraints are MANDATORY:

Backend:
- Python is the required backend language.
- FastAPI for APIs.
- SQLModel for data modeling.
- Neon DB for relational persistence (when persistence is introduced).

Frontend (later phases):
- Next.js is mandatory for web UI.

AI & Tooling:
- OpenAI Agents SDK for agent orchestration.
- MCP (Model Context Protocol) for tool invocation and integration.

Infrastructure (later phases):
- Docker for containerization.
- Kubernetes for orchestration.
- Kafka for event streaming.
- Dapr for service abstraction and runtime capabilities.

Agents MUST NOT introduce alternative stacks without explicit specification approval.

────────────────────────────────────────
5. ARCHITECTURE & QUALITY PRINCIPLES
────────────────────────────────────────

All phases MUST adhere to the following principles:

- Clean Architecture is mandatory.
- Clear separation of concerns across layers and services.
- Stateless services MUST be used where required.
- State MUST be externalized and explicitly managed.
- Cloud-native readiness MUST be maintained even in local deployments.
- Systems MUST be horizontally scalable where applicable.
- Failure modes MUST be predictable and safe.

────────────────────────────────────────
6. SECURITY, DATA & RELIABILITY
────────────────────────────────────────

- Users own their data exclusively.
- Cross-user data access is forbidden.
- Authentication and authorization MUST be enforced where applicable.
- Secrets MUST NOT be hard-coded.
- Systems MUST be restart-safe and resilient.

────────────────────────────────────────
7. STABILITY & IMMUTABILITY OF CONSTITUTION
────────────────────────────────────────

- This constitution is expected to remain stable across all phases.
- Amendments are allowed ONLY through an explicit constitutional revision process.
- No phase-level spec may weaken or bypass constitutional rules.

────────────────────────────────────────
8. DEFINITION OF VALID WORK
────────────────────────────────────────

Work is considered valid ONLY IF:
- It complies with this constitution.
- It is fully spec-driven.
- It is generated by authorized agents.
- Behavior matches approved specifications.

────────────────────────────────────────
OUTPUT RULES
────────────────────────────────────────

- Write in formal, professional, enforceable English.
- Use MUST / MUST NOT / SHALL language.
- Do NOT include:
  - Code snippets
  - Tutorials
  - Examples
  - Phase-specific implementation details
- Output ONLY the final Markdown content of:
  /sp.constitution.md

Begin now.

## Response snapshot

Created the Evolution of Todo Constitution v1.0.0 at `.specify/memory/constitution.md` with 8 core principles:

1. **Spec-Driven Development** - Immutable chain: Constitution → Specs → Plans → Tasks → Implementation
2. **Agent Behavior & Execution Rules** - Agents execute intent, not define it
3. **Phase Governance & Evolution Control** - Sequential phases, no leakage, backward compatibility
4. **Technology & Platform Constraints** - Python/FastAPI/SQLModel/NeonDB backend, Next.js frontend, OpenAI Agents SDK, Docker/K8s/Kafka/Dapr infrastructure
5. **Architecture & Quality Principles** - Clean Architecture, separation of concerns, cloud-native readiness
6. **Security, Data & Reliability** - User data ownership, no hard-coded secrets, restart-safe systems
7. **Stability & Immutability** - Amendment process required for changes
8. **Definition of Valid Work** - Validity criteria checklist

Plus Governance section with amendment procedure, versioning policy, and compliance review.

## Outcome

- Impact: Created foundational governance document for 5-phase Evolution of Todo project
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md (new, 332 lines)
- Next prompts: /sp.specify for Phase I feature specification
- Reflection: Constitution successfully captures all 8 requested sections with formal MUST/MUST NOT language

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review PASS - all 8 sections present, MUST/MUST NOT language used, no code/tutorials/examples included
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - initial constitution creation

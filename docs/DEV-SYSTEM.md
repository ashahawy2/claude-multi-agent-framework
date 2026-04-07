# Spec-Driven Development System

A structured development process for multi-agent projects. Every non-trivial change gets tracked, specified, and verified.

## Feature Registry

Two-level structure keeps the big picture readable and the details complete.

### Level 1: `docs/FEATURES.md` (Map)

A single table showing all tracked work. One row per feature/bug/refactor.

```markdown
| ID    | Type           | Title                        | Status      | Spec |
|-------|----------------|------------------------------|-------------|------|
| F-001 | User-facing    | Add export to CSV            | in-progress | [spec](plans/F-001-spec.md) |
| F-002 | Infrastructure | Migrate to connection pooling| done        | [spec](plans/F-002-spec.md) |
| B-001 | Bug fix        | Login fails on Safari        | in-review   | [spec](plans/B-001-spec.md) |
| R-001 | Refactor       | Extract validation module    | pending     | -- |
```

**Feature types:**
- **User-facing** -- new capability visible to end users
- **Infrastructure** -- internal plumbing, performance, reliability
- **Configuration** -- settings, environment, deployment changes

### Level 2: `docs/plans/{id}-spec.md` (Detail)

One file per feature with full context: why, what, tasks, evidence, and running notes. Use the template in `docs/SPEC-TEMPLATE.md`.

## Feature ID Convention

Every non-trivial change gets an ID:

| Prefix | Meaning | Example |
|--------|---------|---------|
| `F-{id}` | Feature or enhancement | `F-012` |
| `B-{id}` | Bug fix | `B-003` |
| `R-{id}` | Refactor (no behavior change) | `R-007` |

IDs are assigned sequentially. Include the ID in every commit message related to that work: `F-012: add CSV header row`.

## When to Skip the Full Spec

Not every change needs a 50-line spec. Match effort to scope.

| Scope | Criteria | Process |
|-------|----------|---------|
| **Trivial** | <10 lines, 1 file, obvious fix | Commit with ID. No spec file needed. |
| **Small** | 1-2 files, clear requirements | Minimal 15-line spec: Why + What + Tasks (3-5 rows) |
| **Medium** | 3-5 files, some ambiguity | Standard spec with all sections. Checkpoints between task groups. |
| **Large** | 5+ files, cross-cutting, risky | Full spec with checkpoints, explicit review gates, and rollback plan. |

When in doubt, write the spec. The 5 minutes spent writing it saves 30 minutes of rework.

## Spec Template

See `docs/SPEC-TEMPLATE.md` for the full template. Key sections:

1. **Status** -- current state at a glance
2. **Why** -- the problem or opportunity (not the solution)
3. **What** -- the proposed solution (brief, not implementation detail)
4. **Assumptions** -- what you are taking for granted
5. **Not Doing** -- explicit scope boundaries
6. **Acceptance Criteria** -- how to know it is done
7. **Validation** -- specific commands or checks to run
8. **Tasks** -- the work breakdown (see Task Breakdown below)
9. **Running Notes** -- append-only context for future sessions
10. **Files Affected** -- keep updated as work proceeds
11. **Status History** -- dated log of state changes

## Task Breakdown

### Vertical Slicing

Slice tasks vertically (end-to-end through layers), not horizontally (one layer at a time).

**Bad (horizontal):**
- T1: Write all database migrations
- T2: Write all API endpoints
- T3: Write all UI components

**Good (vertical):**
- T1: Add "create item" -- migration + endpoint + UI
- T2: Add "list items" -- migration + endpoint + UI
- T3: Add "delete item" -- migration + endpoint + UI

Each vertical slice is independently testable and deliverable.

### Task Sizing

| Size | Estimate | Guideline |
|------|----------|-----------|
| **S** | <15 min | Single function, config change, test addition |
| **M** | 15-45 min | One feature slice, one module change |
| **L** | 45-90 min | Cross-module change, requires design decisions |
| **XL** | 90+ min | Break it down further. XL tasks hide complexity. |

### Requirements for Every Task

- **Self-contained**: can be implemented without completing other pending tasks (unless explicitly marked as dependent)
- **Testable**: has a clear verification step
- **Sized**: S, M, L, or XL (if XL, break it down)

### Pipeline Stages

Each task moves through a pipeline:

```
Design -> Implementation -> Validation -> Review
```

| Stage | Who | What Happens |
|-------|-----|--------------|
| **Design** | Architect / Planner | Define approach, identify risks, set acceptance criteria |
| **Implementation** | Domain agent | Write code, update tests |
| **Validation** | QA agent / Author | Run tests, verify acceptance criteria, capture evidence |
| **Review** | Reviewer agent | Check against spec, known bugs, regression risk |

Not every task needs all four stages. Trivial tasks skip Design and Review.

## Handoff Protocol

When spawning an agent for a task, provide ALL of:

| Field | Purpose |
|-------|---------|
| Feature ID | e.g., `F-012` |
| Task ID | e.g., `T3` |
| Spec path | e.g., `docs/plans/F-012-spec.md` |
| Role in pipeline | e.g., "Implementation" or "Validation" |
| Previous stage output | What was decided in Design, or what was built in Implementation |
| Acceptance criteria | What "done" looks like for THIS task |
| Files to read | Specific files the agent needs (do not make them search) |
| What to do when done | Update spec, create follow-up task, or report back |

**Bad handoff:** "Implement the CSV export feature"
**Good handoff:** "F-012 T3: Implement CSV header row. Spec: docs/plans/F-012-spec.md. Previous: T2 added the data query (see src/export.ts:45). Acceptance: header row matches column order in schema.ts. Read: src/export.ts, src/schema.ts. When done: update spec T3 status to in-validation, paste test output in Evidence."

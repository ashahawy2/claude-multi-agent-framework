# {ID}: {Title}

<!-- Copy this template to docs/plans/{id}-spec.md -->
<!-- Replace {ID} with F-001, B-001, or R-001 as appropriate -->

## Status: pending

<!-- One of: pending | design | in-progress | in-validation | in-review | done | blocked -->

## Why

<!-- The problem or opportunity. Focus on WHY this matters, not WHAT you will build. -->
<!-- Bad: "Add a CSV export button" -->
<!-- Good: "Users manually copy data into spreadsheets, causing errors and wasting 20 min/day" -->

## What

<!-- The proposed solution in 2-5 sentences. High-level approach, not implementation detail. -->
<!-- Save implementation detail for the Tasks table. -->

## Assumptions

<!-- What you are taking for granted. If any assumption is wrong, the plan may need to change. -->
<!-- Example: "The users table already has an email column" -->

- 

## Not Doing

<!-- Explicit scope boundaries. What might seem in-scope but is not. -->
<!-- Example: "Not adding PDF export -- that is a separate feature" -->

- 

## Acceptance Criteria

<!-- How to know the feature is done. Observable, testable statements. -->
<!-- Example: "User can download a .csv file with all their data from the dashboard" -->

- [ ] 
- [ ] 
- [ ] 

## Validation

<!-- Specific commands or manual checks to verify the acceptance criteria. -->

```bash
# Example:
# npm test -- --grep "csv export"
# curl -H "Authorization: Bearer $TOKEN" localhost:3000/api/export?format=csv
```

## Tasks

<!-- Break work into vertical slices. Each task should be self-contained and testable. -->
<!-- Pipeline: Design -> Implementation -> Validation -> Review -->
<!-- Size: S (<15 min), M (15-45 min), L (45-90 min), XL (break it down) -->

| ID | Description | Size | Pipeline | Depends on | Status | Evidence |
|----|-------------|------|----------|------------|--------|----------|
| T1 |             |      | Implementation | -- | pending | |
| T2 |             |      | Implementation | -- | pending | |
| T3 |             |      | Validation | T1, T2 | pending | |
| T4 |             |      | Review | T3 | pending | |

<!-- For medium/large features, insert checkpoints between task groups: -->
<!-- CHECKPOINT after T2: Human reviews data layer before UI work begins -->

## Running Notes

<!-- Append-only. Agents add what they learned so the next session does not re-discover it. -->
<!-- Format: **YYYY-MM-DD (agent-name)**: What was learned. -->

## Files Affected

<!-- Update as work proceeds. Helps reviewers and future sessions. -->

| File | Change Type | Task |
|------|-------------|------|
|      |             |      |

## Status History

<!-- Dated log of state changes. -->

| Date | Status | Notes |
|------|--------|-------|
| YYYY-MM-DD | pending | Spec created |

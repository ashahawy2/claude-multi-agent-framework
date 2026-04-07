# Development System

How features go from idea to shipped.

## Feature Registry

### Two-Level Structure

**docs/FEATURES.md** -- The map. Registry with ID, status, type, description.

**docs/plans/F-{id}-spec.md** -- The detail. Spec with criteria, tasks, notes.

### Feature ID Convention

| Prefix | Type | Example |
|--------|------|--------|
| F-{id} | Feature | F-012: Add webhook support |
| B-{id} | Bug fix | B-003: Fix race condition |
| R-{id} | Refactor | R-007: Extract validation |

### Feature Types

| Type | Validated by | Example |
|------|-------------|--------|
| User-facing | E2E tests, manual | Search, dashboard |
| Infrastructure | Unit/integration tests | Rate limiting |
| Configuration | Config validation | CI pipeline |

## When to Skip the Full Spec

| Size | Needed | Example |
|------|--------|--------|
| Trivial (1 file, <10 lines) | Commit with ID | Fix typo |
| Small (1-2 files) | 15-line spec | Edge case fix |
| Medium (3-5 files) | Standard spec | API endpoint |
| Large (5+ files) | Full spec + checkpoints | Cross-domain feature |

## Spec Template

See docs/SPEC-TEMPLATE.md for copy-paste template.

## Task Breakdown

Slice vertically. Each task = working, testable functionality.

| Size | Files | Guidance |
|------|-------|--------|
| S | 1-2 | Single function |
| M | 3-5 | One feature slice |
| L | 5-8 | Consider splitting |
| XL | 8+ | Must break down |

### Pipeline Stages

| Stage | Agent | When |
|-------|-------|-----|
| Design | architect | Before implementation |
| Implementation | backend/frontend/domain-expert | During |
| Validation | qa | After implementation |
| Review | reviewer | Before commit |

## Execution

### Handoff

Include: Feature ID, Task ID, spec path, role, criteria, files, done instructions.

### Task Status

pending -> design -> in-progress -> in-validation -> in-review -> done | blocked

### Verification Evidence

Every done task needs proof. "Seems right" is never sufficient.

## Context Preservation

Running notes survive sessions. Append: approaches, progress, blockers, decisions.

## Urgent Fixes

No hotfix path. Every fix gets B-{id}. Minimal spec = 60 seconds.

## Three Recording Mechanisms

| Mechanism | Direction | Purpose |
|-----------|-----------|--------|
| Specs | Forward | What to do |
| Trackers | Backward | Per-agent history |
| CHANGELOG | Backward | Cross-agent timeline |

## Common Rationalizations

| Excuse | Reality |
|--------|--------|
| "Simple, no spec" | Still needs ID + criteria |
| "Document after" | Value is clarity before code |
| "One line, other domain" | Spawn the right agent |
| "No evidence needed" | Run the test, paste output |

## Enforcement

| What | How | Blocks? |
|------|-----|--------|
| Feature ID | Hook | Warning |
| Files match spec | Reviewer | Yes |
| Evidence column | Reviewer | Yes |
| Spec co-modified | Reviewer | Yes |
| Running notes | Reviewer | Warning |

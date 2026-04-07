# Quality Audit System

AI agents produce artifacts -- code, configuration, prompts, documentation. Without systematic auditing, quality drifts over time: conventions get forgotten, fixed bugs reappear, scope creeps. This document describes a closed-loop system that catches drift early and fixes it efficiently.

---

## The Quality Loop

```
Artifacts (code, config, prompts, docs)
     |
     v
  AUDITOR -- checks against --> Standards + Known Issues + Conventions
     |
     v
  Audit Report (pass/fail per dimension)
     |
     v
  ENHANCER -- targeted fixes --> Updated Artifacts
     |                               |
     v                               v
  Known Issues Registry <----- Lessons learned feed back into agent definitions
```

The loop is continuous: every audit may discover new issues, which get registered in the Known Issues (KI) registry, which future audits check against. Lessons compound over time.

---

## Known Issues (KI) Registry

Location: `.claude/known-issues.md`

Every quality problem discovered through audits, testing, or production use gets a KI entry. This is the project immune system -- it prevents the same class of bug from recurring.

Each entry contains:

| Field | Purpose |
|-------|---------|
| **ID** | `KI-{number}`, sequential |
| **Severity** | Critical / High / Medium |
| **Description** | What went wrong |
| **Affected Artifacts** | Which files/patterns are impacted |
| **Prevention Rule** | The rule that prevents recurrence |
| **Status** | `open` or `resolved` (with date and fix reference) |

**Rules for the registry:**

- Any agent discovering a quality issue MUST add a KI entry
- Before modifying any artifact, check if KI entries reference it
- The auditor agent cross-references every audit against the full KI registry
- Resolved entries stay in the registry -- they document the project history

---

## Auditor Agent

The auditor is read-only. It checks artifacts against a configurable checklist and produces a structured report. It never fixes anything.

### 7 Audit Dimensions

Every audit scores an artifact across these dimensions:

#### 1. Structural Completeness

Are all required sections, fields, or components present? Does the structure match project templates or conventions?

**Examples:** A config file missing required keys. An agent definition missing a tracker protocol section. A module missing error handling.

#### 2. Behavioral Correctness

Does the artifact do what its specification says? Are edge cases handled? Does the logic match the intended behavior?

**Examples:** A validation function that accepts invalid input. A prompt that contradicts its stated behavior. An API endpoint that returns wrong status codes.

#### 3. Regression Check

Cross-reference against the KI registry. Is every relevant known issue addressed? Has a previously fixed problem been reintroduced?

**Examples:** A known issue about missing null checks -- does the artifact have null checks? A KI entry about timezone handling -- is the artifact timezone-aware?

#### 4. Convention Compliance

Do naming conventions, code style, patterns, and project standards match what is defined in `.claude/reference.md` and project configuration?

**Examples:** Inconsistent naming (camelCase vs snake_case). Non-standard file organization. Missing standard headers or comments.

#### 5. Scope Check

Does the artifact contain only what was requested? Are there out-of-scope additions, unauthorized modifications, or unnecessary complexity?

**Examples:** A bug fix that also refactors unrelated code. A feature that adds unrequested configuration options. "Improvements" to adjacent files.

#### 6. Size/Complexity

Is the artifact within project limits for file size, function length, nesting depth, and overall complexity? Is the complexity justified by requirements?

**Examples:** A 500-line function that should be split. Deeply nested conditionals. A configuration file with redundant entries.

#### 7. Documentation

Are changes documented in appropriate places? Do comments explain "why" rather than "what"? Are relevant docs updated?

**Examples:** A new feature with no changelog entry. A complex algorithm with no explanation of its approach. Changed behavior not reflected in user-facing docs.

### Audit Report Format

```
AUDIT REPORT: {artifact name}
Date: {date}
Score: {pass_count}/{total} dimensions passed

PASSED:
- {dimension}: {brief note}

FAILED:
- {dimension}: {what failed, where, severity}

WARNINGS:
- {dimension}: {concern, not blocking}

KI MATCHES:
- KI-{id}: {whether addressed or not}

RECOMMENDATIONS:
1. {specific fix with file/line reference}
```

---

## Enhancement Agent

The enhancer receives an audit report and makes targeted fixes. It follows strict rules:

1. **Read first.** Understand the full artifact before making any change
2. **Fix only what the audit flagged.** No unrelated improvements
3. **Preserve existing patterns.** Match the existing conventions of the artifact
4. **Maximum 2 cycles.** If the artifact still fails audit after 2 fix rounds, escalate to the user
5. **Write positive patterns.** Describe what TO do, not just what NOT to do
6. **Document every change.** Before/after, referencing which audit finding each change addresses

### Fix Cycle

```
Audit Report
     |
     v
Enhancer reads artifact + report + KI entries
     |
     v
Targeted fixes (cycle 1)
     |
     v
Re-audit
     |
     +--[pass]--> Done
     |
     +--[fail]--> Targeted fixes (cycle 2)
                       |
                       v
                  Re-audit
                       |
                       +--[pass]--> Done
                       |
                       +--[fail]--> Escalate to user
```

---

## Drift Prevention

Artifacts drift from their specs and standards over time, especially when multiple agents modify them across sessions. Drift prevention catches this before it becomes a problem.

### Scheduled Audits

Run audits on a regular cadence, not just when changes are made. Frequency depends on how actively artifacts change:

- **High-churn artifacts** (frequently modified code, prompts): audit after every significant change
- **Stable artifacts** (configuration, architecture docs): audit weekly or on-demand
- **Templates and conventions**: audit when onboarding new components or agents

### KI Drift Alerts

When a new KI entry is added, check whether existing artifacts are affected. A new KI entry means a new class of problem has been discovered -- all relevant artifacts should be audited against it.

### Coverage Checks

Track which artifacts have been audited and when. Flag artifacts that have not been audited within the expected cadence. This prevents "forgotten corners" where quality silently degrades.

---

## Scoring (Optional)

For projects that use LLM-as-judge evaluation, audit scoring dimensions should be configurable rather than hardcoded. Store scoring criteria in project configuration (config files or database) so they can be tuned per project.

Configurable aspects:

- **Dimension weights**: Which of the 7 dimensions matter most for this project
- **Pass thresholds**: What score constitutes a pass vs. warning vs. failure
- **Custom dimensions**: Project-specific quality checks beyond the standard 7
- **Severity mapping**: How audit findings map to severity levels

This allows the same audit framework to serve different projects with different quality priorities.

---

## Getting Started

1. Create `.claude/known-issues.md` with the empty registry template
2. Add `quality-auditor` and `quality-enhancer` to your agent roster in `CLAUDE.md`
3. Run an initial audit of your most critical artifacts to establish a baseline
4. Add KI entries for any issues found
5. Set up a cadence for regular audits based on your project change velocity

The quality system is optional and additive -- it layers on top of the existing agent framework without requiring changes to how other agents work.

# Development Workflow Skills

## The Pattern

Instead of ad-hoc instructions ("fix the login bug", "add a search feature"), development work enters through structured skills. Each skill enforces the right process — spec creation, agent routing, verification, and tracking.

Skills are the entry points. They gate work so the orchestrator can't skip steps.

## Why Skills Matter

Without skills, the orchestrator shortcuts:
- "This is simple, I'll just fix it" → skips spec, skips review, skips tracking
- "I'll document later" → documentation never happens
- "Just one quick change" → scope creeps, no acceptance criteria

Skills make the process automatic. The user types `/feature` and the spec is created before any code is written. No willpower required.

## Skill Routing Table

| User Intent | Skill | What It Does |
|-------------|-------|-------------|
| New feature or enhancement | `/feature` | Idea refinement → spec creation → FEATURES.md entry → agent spawning |
| Bug fix or production error | `/bug` | Minimal B-{id} spec → immediate agent spawn → regression entry |
| Refactor or restructure | `/refactor` | Chesterton's Fence check → behavior preservation spec → agents |
| Resume tracked work | `/implement` | Read spec → find unblocked tasks → spawn agents in parallel |
| Pre-commit code review | `/review` | Spawn reviewer agent against spec + staged changes |
| Finalize and commit | `/ship` | Verify evidence → run tests → update status → commit |
| Check progress | `/status` | Dashboard: in-progress, stale, blocked, parallel opportunities |
| Debug or investigate | `/debug` | Systematic diagnosis → hypothesis → evidence → report (no fixes) |

## How to Implement Skills

Skills in Claude Code are custom slash commands. Each skill is a markdown file in `.claude/commands/` that contains the prompt template the orchestrator follows.

### Example: `/feature` skill

Create `.claude/commands/feature.md`:

```markdown
# Feature Skill

The user wants to build a new feature. Follow this process:

## Step 1: Refine
Ask the user to describe the feature. Clarify:
- What problem does it solve?
- Who is affected?
- What does "done" look like?

## Step 2: Spec
Create a spec file at `docs/plans/F-{next_id}-spec.md` using the template from `docs/SPEC-TEMPLATE.md`.
Fill in: Why, What, Assumptions, Acceptance Criteria.

## Step 3: Register
Add an entry to `docs/FEATURES.md` with the new F-{id}.

## Step 4: Break Down
Create tasks in the spec's task table. Each task has a pipeline of agents.

## Step 5: Execute
Spawn the first unblocked task's agent(s). Provide full context from the spec.

## Step 6: Track
After each task completes, update the spec (status, evidence, running notes).
```

### Example: `/bug` skill

Create `.claude/commands/bug.md`:

```markdown
# Bug Fix Skill

The user has reported a bug. Follow this process:

## Step 1: Classify
- What's the symptom?
- Can it be reproduced?
- What's the severity?

## Step 2: Minimal Spec
Create `docs/plans/B-{next_id}-spec.md` with:
- Why (the symptom and impact)
- Files Affected (best guess)
- One task: diagnose and fix

## Step 3: Diagnose First
Spawn the appropriate domain agent to DIAGNOSE (not fix) the issue.
Read the diagnosis before approving a fix.

## Step 4: Fix
Once root cause is confirmed, spawn the agent to fix it.

## Step 5: Verify
Run tests. Fill Evidence column. Spawn reviewer.

## Step 6: Prevent
Add the bug to `.claude/reference.md` Fixed Bugs table with a prevention rule.
```

## Anti-Rationalization Rules

Skills exist because agents rationalize skipping process. These are NOT valid excuses:

| Rationalization | Reality |
|---|---|
| "This is a one-line fix" | One-line fixes still need an ID and evidence |
| "I'll create the spec after I code it" | That's documentation, not specification. The value is clarity BEFORE code |
| "The user seems urgent" | Urgency is not permission to skip. A minimal spec takes 60 seconds |
| "This is just a refactor" | Refactors need Chesterton's Fence checks. They need R-{id} |
| "I already know what to do" | Your context window is finite. The spec survives session boundaries |
| "The reviewer will catch problems" | The reviewer is the last gate, not the only gate |
| "It's just one line in another domain" | That's how domain violations start. Spawn the right agent |
| "This doesn't need evidence" | "Seems right" is never sufficient. Run the test, paste the output |

## Adapting for Your Project

1. **Start with 3 skills:** `/feature`, `/bug`, `/review`
2. **Add as needed:** `/refactor`, `/ship`, `/status` when your project grows
3. **Customize prompts:** Each skill's markdown file is a prompt template -- edit it to match your workflow
4. **The key insight:** Skills are guardrails, not bureaucracy. They take seconds and prevent hours of rework

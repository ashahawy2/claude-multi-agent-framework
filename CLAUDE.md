# Multi-Agent Orchestrator — Claude Code Rules

> **STOP -- READ THIS FIRST, EVERY SESSION, INCLUDING CONTEXT RECOVERY.**
>
> **This project uses specialist agents.** Before doing ANY non-trivial work, you MUST:
> 1. Determine which agent(s) the task needs (see routing table below)
> 2. For **single-agent tasks**: spawn via Task tool with `subagent_type: "general-purpose"`, include the agent's `.claude/agents/<name>.md` content as instructions
> 3. For **multi-agent tasks**: use **TeamCreate** to create a team, then spawn each agent as a teammate. The team tools (TaskCreate, TaskUpdate, SendMessage) handle all coordination automatically
> 4. For **trivial tasks** (fix a typo, read a file, answer a question): handle directly, no agent needed
>
> **Do NOT do domain work yourself. You are the orchestrator.**
>
> **BEFORE implementing ANY fix or feature that touches more than one file, you MUST:**
> 1. **Run impact analysis** -- use Explore agents to trace the full data flow of proposed changes
> 2. **Consult ALL affected domain agents** -- spawn architect + domain-expert + reviewer (at minimum) to review the proposed approach BEFORE writing code
> 3. **Do NOT propose a fix plan to the user until agents have reviewed it.** Your initial analysis is often wrong or incomplete. The agents exist because domain expertise matters.
> 4. **Synthesize agent feedback into a consensus plan** -- present conflicting opinions transparently. If agents disagree, surface the disagreement to the user.
>
> **Why this matters:** The orchestrator sees the surface problem. Domain agents find the root cause. Skipping agent review leads to symptom-level fixes that miss the real issue.

---

## Agent Roster

| Agent | File | Domain | Tracker |
|-------|------|--------|---------|
| **architect** | `.claude/agents/architect.md` | Cross-cutting design, dependency map, schema consistency | `.claude/trackers/architect-tracker.md` |
| **frontend** | `.claude/agents/frontend.md` | UI components, CSS, client-side state, rendering | `.claude/trackers/frontend-tracker.md` |
| **backend** | `.claude/agents/backend.md` | API, services, database, server-side logic | `.claude/trackers/backend-tracker.md` |
| **domain-expert** | `.claude/agents/domain-expert.md` | Business logic, domain rules, validation, prompts | `.claude/trackers/domain-expert-tracker.md` |
| **reviewer** | `.claude/agents/reviewer.md` | Code review, constraint checking, regression prevention | `.claude/trackers/reviewer-tracker.md` |
| **qa** | `.claude/agents/qa.md` | E2E testing, browser automation, regression testing | `.claude/trackers/qa-tracker.md` |

## Auto-Routing

When the user describes a task, route it automatically. The user should never need to name an agent.

| If the task involves... | Route to |
|------------------------|----------|
| React, Vue, Angular, CSS, components, UI, layout, styling | **frontend** |
| API, endpoints, database, SQL, services, middleware, auth | **backend** |
| Business rules, domain logic, validation, prompts, workflows | **domain-expert** |
| Architecture, cross-cutting changes, dependency tracing, schema alignment | **architect** |
| Code review, PR review, audit changes, check for regressions | **reviewer** |
| E2E testing, browser testing, test the app, verify the flow, QA | **qa** |
| Multiple of the above | **TeamCreate** with relevant agents |

## When to Use TeamCreate

| Scenario | Approach |
|----------|----------|
| Task fits **one domain** (e.g., "fix the CSS overlap") | Spawn one agent via Task tool |
| Task spans **multiple domains** (e.g., "add a new API endpoint with UI") | **TeamCreate** → spawn agents as teammates |
| Task needs **sequential handoff** (e.g., "fix the bug then test it") | TeamCreate with backend + qa agents, use `addBlockedBy` |
| Task needs **parallel investigation** (e.g., "why is X broken?") | TeamCreate with architect + backend + domain-expert |
| **Trivial task** (fix a typo, read a file) | Handle directly, no agent |

**After a team completes work**: each agent updates its own tracker file (persistent across sessions) and appends to `.claude/CHANGELOG.md`.

---

## Tracker Updates -- MANDATORY

> **Every fix, feature, or investigation MUST be recorded.** This is non-negotiable.

1. **Agents** update their own tracker (`.claude/trackers/<agent>-tracker.md`) and append to `.claude/CHANGELOG.md` before finishing.
2. **Orchestrator (you)**: if you do work directly (without spawning an agent), YOU must update the relevant tracker and changelog yourself. No work should go untracked.
3. **Format**: Completed entries use `- **YYYY-MM-DD**: <one-line summary>. Files: <list>. Verified: <how>.`
4. **When**: Update trackers immediately after verifying a fix works -- not "later", not "at the end of the session".

---

## Universal Rules (All Agents Follow These)

### Think Before Coding
- State assumptions explicitly. If uncertain, ask -- don't guess silently
- Multiple interpretations? Present them. Don't pick one without saying so
- Simpler approach exists? Say so. Push back when warranted

### Simplicity First
- No features beyond what was asked
- No abstractions for single-use code
- No error handling for impossible scenarios
- If 200 lines could be 50, rewrite it

### Surgical Changes
- Don't "improve" adjacent code, comments, or formatting
- Don't refactor things that aren't broken
- Match existing style, even if you'd do it differently
- Remove imports/variables/functions that YOUR changes made unused
- Every changed line should trace directly to the user's request

### Goal-Driven Execution
- "Add validation" -> write tests for invalid inputs, then make them pass
- "Fix the bug" -> write a test that reproduces it, then make it pass
- For multi-step tasks, state a brief plan with verify steps

### Verify Before Writing Code
- Read the source file -- confirm exact signatures, field names, return types
- Check types at boundaries -- caller vs callee, Optional vs required
- Grep before creating -- the function may already exist
- Trace the full call chain

### Honest Testing
- Workaround = BUG, not success
- Hung/timed-out request = failure
- Generic output = BROKEN
- Testing finds bugs, not proves success

### Code Hygiene
- No `print()` -- use `logging` module (Python) or `console.warn/error` (JS)
- No hardcoded paths
- No mock/fallback responses in production handlers -- return errors
- No silent exceptions -- log at minimum
- No commented-out code -- git has history

---

## Reference: Naming Conventions

> Customize this section with YOUR project's naming conventions.

| Domain | Convention | Example |
|--------|-----------|---------|
| Database columns | snake_case | `user_name`, `created_at` |
| API endpoints | kebab-case | `/api/user-profile` |
| React components | PascalCase | `UserProfile`, `DashboardPanel` |
| CSS classes | kebab-case | `.user-profile`, `.dashboard-panel` |
| Environment variables | SCREAMING_SNAKE | `DATABASE_URL`, `API_KEY` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |

## Reference: Fixed Bugs -- Do NOT Reintroduce

> Add your project's known bugs here. Every agent and the reviewer check this list.

| Bug | Rule |
|-----|------|
| _Example: `user.age` crash_ | _`UserProfile` has no `age` field, use `user.date_of_birth`_ |
| _Example: SQL injection in search_ | _Always use parameterized queries, never string interpolation_ |

## Reference: Existing Features -- Do NOT Reimplement

> Document existing implementations to prevent duplication.

| Feature | Location |
|---------|----------|
| _Example: Authentication_ | _`src/auth/`_ |
| _Example: Email service_ | _`src/services/email.py`_ |

## Reference: High-Level Dependency Map

> Customize with YOUR project's architecture.

```
Frontend (React/Vue/Angular) --> API Layer (REST/GraphQL)
  --> Service Layer (business logic)
    --> Data Layer (ORM/DB queries)
      --> Database (PostgreSQL/MySQL/SQLite)

External Services:
  --> Email (SendGrid/SES)
  --> Storage (S3/GCS)
  --> Auth (OAuth/JWT)
```

---

## Changelog

`.claude/CHANGELOG.md` -- Append-only log of all completed work. Agents write here when tasks finish.

# Claude Code Multi-Agent Framework

A battle-tested framework for orchestrating specialist AI agents in [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Distribute complex software engineering work across domain-specific agents that coordinate via shared task lists, inter-agent messaging, and persistent trackers.

**Why this exists:** A single Claude Code session has a finite context window. Complex projects exceed it. This framework splits work across specialist agents that each operate in their own context, coordinated by an orchestrator that never does domain work itself.

---

## Quick Start

1. Copy `.claude/` into your project root
2. Customize `CLAUDE.md` with your project's architecture, conventions, and known bugs
3. Customize each agent in `.claude/agents/` with your domain knowledge
4. Enable agent teams: add `"env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }` to your Claude Code settings
5. Start Claude Code. The orchestrator auto-routes tasks to the right agents.

---

## Architecture Overview

```
User Request
     |
     v
ORCHESTRATOR (CLAUDE.md)
  |  Never does domain work itself.
  |  Routes tasks, spawns agents, synthesizes results.
  |
  +---[single-domain task]----> spawn ONE agent via Task tool
  |
  +---[multi-domain task]-----> TeamCreate + spawn agents as teammates
  |                             Agents coordinate via shared TaskList + SendMessage
  |
  +---[trivial task]----------> handle directly (fix typo, read file, answer question)
```

### Agent Roster

| Agent | Domain | Writes Code? | Key Skill |
|-------|--------|-------------|-----------|
| **architect** | System design, dependency mapping, schema consistency | No (advisory) | Traces data flow end-to-end |
| **frontend** | UI components, CSS, client-side state | Yes | Component development |
| **backend** | API, services, database, server-side logic | Yes | Service implementation |
| **domain-expert** | Business logic, domain rules, prompt engineering | Yes (prompts/config) | Subject matter expertise |
| **qa** | E2E testing, browser automation, regression testing | No (tests only) | Finds bugs, not proves success |
| **reviewer** | Code review, constraint checking, regression prevention | No (read-only) | Catches what others miss |

### How Context Is Minimized

| Technique | How It Works |
|-----------|-------------|
| **Agent specialization** | Each agent loads only its domain knowledge (50-150 lines), not the full project |
| **Tracker persistence** | Work history lives in `.claude/trackers/`, survives context resets |
| **Task delegation** | Orchestrator returns clean summaries, messy exploration stays in agent context |
| **Parallel execution** | Independent agents run simultaneously, each in their own context window |
| **CHANGELOG as memory** | Completed work is compressed into one-line summaries in `.claude/CHANGELOG.md` |

---

## Directory Structure

```
your-project/
  CLAUDE.md                          # Orchestrator instructions (loaded every session)
  .claude/
    agents/
      architect.md                   # System architect agent definition
      frontend.md                    # Frontend specialist agent definition
      backend.md                     # Backend specialist agent definition
      domain-expert.md               # Domain/SME specialist agent definition
      qa.md                          # QA and testing agent definition
      reviewer.md                    # Code reviewer agent definition
    trackers/
      architect-tracker.md           # Persistent work log for architect
      frontend-tracker.md            # Persistent work log for frontend
      backend-tracker.md             # Persistent work log for backend
      domain-expert-tracker.md       # Persistent work log for domain expert
      qa-tracker.md                  # Persistent work log for QA
      reviewer-tracker.md            # Persistent work log for reviewer
    CHANGELOG.md                     # Append-only log of all completed work
    prompt-contracts.md              # Non-negotiable system behaviors (optional)
    settings.local.json              # Claude Code settings with team features enabled
```

---

## How It Works

### 1. The Orchestrator (CLAUDE.md)

The orchestrator is NOT an agent file -- it's the main `CLAUDE.md` that Claude Code loads on every session. It:

- **Routes tasks** to the correct agent(s) based on keywords
- **Spawns agents** via the `Task` tool (single-domain) or `TeamCreate` (multi-domain)
- **Synthesizes results** from multiple agents into a coherent response
- **Never does domain work itself** -- it delegates, coordinates, and reports

### 2. Single-Domain Tasks

When a task fits one agent's domain, spawn it directly:

```
User: "Fix the CSS overlap on the dashboard"
Orchestrator: [spawns frontend agent via Task tool]
Frontend agent: [reads tracker, fixes CSS, updates tracker + CHANGELOG]
Orchestrator: [reports result to user]
```

### 3. Multi-Domain Tasks (Teams)

When a task spans domains, create a team:

```
User: "Add a new API endpoint with UI and tests"
Orchestrator:
  1. TeamCreate("feature-xyz")
  2. TaskCreate: "Implement /api/xyz endpoint" → assign to backend
  3. TaskCreate: "Build XyzPanel component" → assign to frontend (blocked by backend)
  4. TaskCreate: "E2E test the new feature" → assign to qa (blocked by frontend)
  5. TaskCreate: "Review all changes" → assign to reviewer (blocked by qa)
Agents:
  - backend completes → unblocks frontend
  - frontend completes → unblocks qa
  - qa tests → unblocks reviewer
  - reviewer audits → reports findings
Orchestrator: [synthesizes team results, reports to user]
```

### 4. Impact Analysis (Before Any Fix)

Before implementing fixes that touch multiple files:

```
1. Run Explore agents to trace the full data flow of proposed changes
2. Spawn architect + domain-expert + reviewer to review the approach
3. Wait for agent feedback BEFORE writing code
4. Synthesize agent input into a consensus plan
5. Present plan to user, surface any disagreements
```

**Why:** The orchestrator sees the surface problem. Domain agents find the root cause. Skipping agent review leads to symptom-level fixes.

### 5. Persistent Memory (Trackers + CHANGELOG)

Every agent updates two files when it completes work:

1. **Its own tracker** (`.claude/trackers/<agent>-tracker.md`): In-progress, pending, blocked, completed
2. **Shared CHANGELOG** (`.claude/CHANGELOG.md`): Append-only log with date, problem, fix, files, verification

This means:
- New sessions pick up where the last left off
- No work is ever lost or forgotten
- Any agent can see what other agents have done

---

## Customization Guide

### Step 1: Define Your Agents

Edit each file in `.claude/agents/`. Each agent needs:

1. **Identity** -- who they are, what they own
2. **Tracker protocol** -- how they read/update their tracker (use the template)
3. **Domain knowledge** -- architecture, schemas, key files, conventions
4. **Known bugs** -- things they must never reintroduce
5. **Rules** -- coding standards specific to their domain

### Step 2: Customize the Orchestrator (CLAUDE.md)

Edit `CLAUDE.md` to include:

1. **Agent roster** -- table of agents, files, domains
2. **Auto-routing table** -- keywords → agent mapping
3. **Universal rules** -- coding standards that apply to ALL agents
4. **Known bugs** -- project-wide bugs that no agent should reintroduce
5. **Naming conventions** -- field names, ID formats, enum values
6. **Dependency map** -- how your system's layers connect

### Step 3: Set Up Trackers

Each tracker starts empty with the standard sections:
- In Progress
- Pending (prioritized backlog)
- Blocked (with reason and which agent can unblock)
- Completed (append-only log)

### Step 4: Enable Teams

Add to your Claude Code settings (`~/.claude/settings.json` or project `.claude/settings.local.json`):

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## Design Principles

### 1. Orchestrator Never Does Domain Work

The orchestrator's job is routing, coordination, and synthesis. If it starts writing code, debugging services, or designing UI, it's doing the agent's job and wasting its own context window.

### 2. Agents Are Stateless Per Session, Stateful Via Trackers

Each agent spawn starts fresh. Persistent state lives in tracker files that agents read at session start and update at session end. This is how work survives across context resets.

### 3. Read Before Writing

Every agent MUST read source files before modifying them. No guessing at function signatures, field names, or return types. Verify types at every boundary.

### 4. Impact Analysis Before Implementation

Before any multi-file change: trace the data flow, consult affected agents, wait for feedback. Your initial analysis is often wrong or incomplete.

### 5. Honest Testing

- Workaround = BUG, not success
- Hung/timed-out request = failure
- Generic output = BROKEN
- Testing finds bugs, not proves success

### 6. Tracker Updates Are Mandatory

No work goes untracked. Every fix, feature, or investigation gets a one-line entry in the agent's tracker and the shared CHANGELOG. This is the project's memory.

---

## Patterns & Anti-Patterns

### Pattern: Sequential Handoff

```
backend builds feature → creates task for qa → qa tests → creates task for reviewer
```

Use `addBlockedBy` in TaskCreate to enforce ordering.

### Pattern: Parallel Investigation

```
architect traces data flow  }
domain-expert checks rules  }  simultaneously
reviewer audits constraints }
```

Spawn all three agents at once. Synthesize their findings.

### Pattern: Fix-Then-Verify

```
backend fixes bug → qa runs regression test → reviewer audits the fix
```

Backend creates follow-up tasks for qa and reviewer before marking its own task complete.

### Anti-Pattern: Orchestrator Does Domain Work

```
User: "Fix the mastery calculation"
BAD: Orchestrator reads the code, edits the formula
GOOD: Orchestrator spawns backend agent (for the fix) + domain-expert (for the formula) + reviewer (for audit)
```

### Anti-Pattern: Skipping Agent Review

```
User: "Tutor repeats questions"
BAD: Orchestrator analyzes prompts, proposes a prompt fix
GOOD: Orchestrator consults domain-expert (finds the pipeline bug causing repetition)
      + architect (finds the planner routing gap)
      + reviewer (checks for regressions)
```

### Anti-Pattern: Fire and Forget

```
BAD: Agent fixes bug, doesn't update tracker
GOOD: Agent fixes bug, updates tracker with date/files/verification, appends to CHANGELOG
```

---

## Advanced Topics

### Prompt Contracts

For systems with LLM prompts, define non-negotiable behaviors in `.claude/prompt-contracts.md`. These are rules that must hold regardless of prompt changes. The reviewer agent checks them on every prompt modification.

### Known Bugs Registry

Maintain a table of fixed bugs in CLAUDE.md with rules for prevention. Every agent and the reviewer check this list before making changes. This prevents regression loops.

### Cost Optimization

- Route simple tasks to `model: "haiku"` for faster, cheaper execution
- Use `subagent_type: "Explore"` for read-only research (cheaper than general-purpose)
- Limit teams to 3-4 agents maximum for practical coordination
- Use the `run_in_background` parameter for independent agents

### When NOT to Use This Framework

- Solo developer on a small project (< 10 files)
- Tasks that take < 5 minutes
- Pure research/exploration (use a single Explore agent instead)
- Projects without clear domain boundaries

---

## FAQ

**Q: Do I need all 6 agents?**
A: No. Start with 3 (backend + frontend + reviewer) and add more as your project grows. The domain-expert and architect agents add value on larger projects.

**Q: Can I add custom agents?**
A: Yes. Create a new `.md` file in `.claude/agents/`, add a tracker in `.claude/trackers/`, and update the routing table in `CLAUDE.md`.

**Q: How do agents communicate?**
A: Via `SendMessage` (direct messages), shared `TaskList` (work queue with dependencies), and tracker files (persistent state).

**Q: What happens when agents disagree?**
A: The orchestrator surfaces the disagreement to the user. It doesn't pick a winner silently.

**Q: Does this work without team features enabled?**
A: Partially. You can still spawn single agents via the `Task` tool. Teams require `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

---

## License

MIT -- Use, modify, and share freely. Attribution appreciated.

## Contributing

PRs welcome. If you've battle-tested a pattern in production, share it.

# Orchestration Patterns

Practical patterns for coordinating multi-agent work in Claude Code.

---

## Pattern 1: Hub-and-Spoke (Most Common)

The orchestrator creates a team, assigns tasks, and synthesizes results.

```
         Orchestrator
        /     |      \
   Backend  Frontend  QA
```

**When to use:** Most multi-domain tasks.

**How:**
1. `TeamCreate("feature-xyz")`
2. Create tasks with `TaskCreate` and assign to agents
3. Agents work independently, update trackers
4. Orchestrator synthesizes results for the user

---

## Pattern 2: Sequential Pipeline

Tasks flow in order with explicit dependencies.

```
Backend -> Frontend -> QA -> Reviewer
```

**When to use:** Feature implementation where each step depends on the previous.

**How:**
1. Create all tasks up front
2. Use `addBlockedBy` to enforce ordering:
   - Frontend task blocked by Backend task
   - QA task blocked by Frontend task
   - Reviewer task blocked by QA task
3. As each agent completes, the next is automatically unblocked

**Example:**
```
Task 1: "Implement /api/users endpoint" → backend
Task 2: "Build UserList component" → frontend (blockedBy: [1])
Task 3: "E2E test user list page" → qa (blockedBy: [2])
Task 4: "Review all changes" → reviewer (blockedBy: [3])
```

---

## Pattern 3: Parallel Investigation

Multiple agents investigate the same problem from different angles.

```
    Orchestrator
   /     |      \
Architect  Backend  Domain-Expert
   \     |      /
    Synthesis
```

**When to use:** Debugging complex issues where the root cause isn't obvious.

**How:**
1. Spawn 2-3 agents in parallel, each investigating from their domain perspective
2. Each returns their findings
3. Orchestrator synthesizes: "Architect says X, Backend says Y, Domain-Expert says Z"
4. Present all perspectives to the user

**Key insight:** Different agents see different root causes. The architect sees dependency issues, the backend sees data flow bugs, the domain expert sees business logic violations. All three may be right.

---

## Pattern 4: Fix-Then-Verify

Implementation agent fixes, QA agent verifies, reviewer audits.

```
Backend (fix) -> QA (verify) -> Reviewer (audit)
```

**When to use:** Bug fixes that need regression testing and code review.

**How:**
1. Backend/Frontend agent implements the fix
2. Agent creates follow-up task for QA: "Verify fix for bug X"
3. QA runs regression tests
4. QA creates follow-up task for Reviewer: "Review fix for bug X"
5. Reviewer audits the changes

---

## Pattern 5: Competing Solutions

Multiple agents propose solutions to the same problem.

```
    Problem
   /       \
Agent A   Agent B
   \       /
   Comparison
```

**When to use:** Design decisions where there are multiple valid approaches.

**How:**
1. Spawn 2 agents with the same problem but different constraints
2. Each proposes a solution
3. Orchestrator compares approaches:
   - Complexity
   - Performance
   - Maintainability
   - Alignment with existing patterns
4. Present both options to the user with trade-offs

---

## Pattern 6: Incremental Delivery

Break a large feature into small, verifiable increments.

```
Sprint 1: Backend API  -> verify
Sprint 2: Frontend UI  -> verify
Sprint 3: Integration  -> verify
Sprint 4: Polish + QA  -> verify
```

**When to use:** Large features that would exceed a single agent's context.

**How:**
1. Plan the increments with architect agent
2. Execute each increment as a separate team session
3. Each increment ends with verification
4. Tracker files carry state between increments

---

## Anti-Patterns

### Don't: Orchestrator Does Domain Work

**BAD:** User asks to fix a CSS bug. Orchestrator reads the CSS file and makes changes.
**GOOD:** Orchestrator spawns frontend agent who reads the CSS, understands the layout context, and makes minimal changes.

### Don't: Skip Impact Analysis

**BAD:** User asks to change a field name. Orchestrator renames it in one file.
**GOOD:** Orchestrator spawns architect to trace all usages, then spawns backend/frontend agents to rename consistently.

### Don't: Fire and Forget

**BAD:** Agent fixes a bug and says "done" without updating tracker.
**GOOD:** Agent fixes bug, updates tracker with date/files/verification, appends to CHANGELOG.

### Don't: Spawn Too Many Agents

**BAD:** Create a 6-agent team for a simple CSS fix.
**GOOD:** Spawn one frontend agent. Use teams only when work spans multiple domains.

### Don't: Let Agents Work Without Constraints

**BAD:** "Fix the performance issues" with no context.
**GOOD:** "Optimize the /api/users query -- it's returning 500ms response times. The query is in user_repository.py:45. Current index setup is in migration_003.sql."

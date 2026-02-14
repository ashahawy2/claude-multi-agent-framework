# Best Practices

Lessons learned from running multi-agent workflows in production Claude Code projects.

---

## 1. Agent Design

### Keep Agent Definitions Focused

Each agent definition should be **100-150 lines**. If it's longer, you're probably including information the agent doesn't need.

**Good:** Backend agent knows the database schema and API patterns.
**Bad:** Backend agent knows the CSS architecture and component hierarchy.

### Include Domain-Specific Knowledge

The value of an agent comes from its domain expertise. A generic "backend agent" is barely better than no agent at all. A backend agent that knows YOUR database schema, YOUR API conventions, and YOUR known bugs is extremely valuable.

### Document Known Bugs Per Agent

Each agent should have a "Known Bugs" section listing bugs in their domain that must never be reintroduced. This prevents the most common regression pattern: an agent fixing one thing while accidentally reintroducing a previously fixed bug.

---

## 2. Orchestration

### The Orchestrator is a Router, Not a Worker

The CLAUDE.md orchestrator should NEVER:
- Read source files to understand implementation details
- Write code to fix bugs
- Design API schemas
- Debug CSS layout issues

It SHOULD:
- Route tasks to the right agent(s)
- Spawn teams for multi-domain tasks
- Synthesize agent results into user-facing summaries
- Surface disagreements between agents

### Always Run Impact Analysis First

Before ANY multi-file change:
1. Spawn an Explore agent to trace the data flow
2. Consult affected domain agents
3. Wait for feedback before proposing a plan

This catches root causes that surface-level analysis misses.

### Surface Disagreements, Don't Resolve Them

When agents disagree about an approach, present both perspectives to the user. Don't silently pick the one that seems more reasonable -- domain expertise matters, and you (the orchestrator) aren't a domain expert.

---

## 3. Teams

### Limit Team Size to 3-4 Agents

More agents = more coordination overhead. For most tasks, 3-4 agents is optimal:
- 2 implementation agents (e.g., backend + frontend)
- 1 verification agent (qa or reviewer)
- 1 advisory agent (architect or domain-expert) -- optional

### Use Dependency Chains

Always use `addBlockedBy` to enforce task ordering. Don't rely on agents checking manually:

```
Task: "Build API endpoint" → backend
Task: "Build UI component" → frontend (blockedBy: ["Build API endpoint"])
Task: "E2E test" → qa (blockedBy: ["Build UI component"])
```

### Clean Up Teams After Completion

After a team finishes:
1. Verify all tasks are completed or explicitly deferred
2. Send shutdown requests to all agents
3. Delete the team with `TeamDelete`

---

## 4. Trackers

### Update Trackers Immediately

Tracker updates happen RIGHT AFTER verification, not "when you get around to it." If an agent crashes mid-session, only the work recorded in the tracker survives.

### Use One-Line Summaries

Tracker entries should be scannable. One line per completed task:

```markdown
- **2026-01-15**: Fixed mastery calculation to use display_mastery. Files: tracker.py, planner.py. Verified: E2E test PASS.
```

Not:
```markdown
- **2026-01-15**: I investigated the mastery calculation issue and found that the raw EMA value was being used instead of the display mastery (which is the average of procedural, conceptual, and transfer mastery). I traced the call chain through 5 files and found 3 locations where the wrong formula was used. I updated all 3 locations to use the centralized display_mastery method. I then verified by running the E2E test suite which confirmed that the welcome screen now shows the correct mastery percentage. Files affected: tracker.py (line 42, 67), planner.py (line 234), service.py (line 89). The fix was verified by comparing the welcome screen percentage with the API response.
```

### Use "Blocked" Actively

When an agent can't proceed, it should move the task to "Blocked" with:
- What it's blocked on
- Which agent can unblock it
- What the blocker needs to do

This turns ambiguous dependencies into actionable items.

---

## 5. CHANGELOG

### Organize by Date, Then by Agent

```markdown
## 2026-01-15

### Backend -- API endpoint fix (backend agent)
- **2026-01-15**: Fixed /api/users to return paginated results. Files: user_routes.py. Verified: curl test.

### Frontend -- User list pagination (frontend agent)
- **2026-01-15**: Added pagination controls to UserList. Files: UserList.jsx. Verified: manual click-through.
```

### Include Problem, Fix, Files, and Verification

Every entry should answer:
1. What was the problem?
2. What was done?
3. What files were changed?
4. How was it verified?

---

## 6. Cost Optimization

### Use Haiku for Simple Tasks

The `model: "haiku"` parameter in the Task tool routes to a faster, cheaper model. Use it for:
- File searches and exploration
- Simple code changes with clear instructions
- Reading and summarizing files

### Use Explore Agents for Research

`subagent_type: "Explore"` creates a read-only agent that can't edit files. It's perfect for:
- Tracing call chains
- Finding all usages of a function
- Understanding how a feature works

It's cheaper and faster than a general-purpose agent.

### Don't Over-Team

A single agent is fine for:
- CSS fixes
- Simple bug fixes
- Adding a single function
- Renaming a variable

Teams are for work that genuinely spans multiple domains.

---

## 7. Prompt Contracts (For AI Projects)

If your project uses LLM prompts:

### Define Contracts Before You Need Them

Don't wait for a regression to define prompt contracts. Document the behaviors that MUST hold from the start.

### The Reviewer Checks Contracts

Every prompt change goes through the reviewer agent, which cross-references against `.claude/prompt-contracts.md`. This catches silent regressions where a "cleanup" removes a critical guardrail.

### Examples > Rules in Prompts

This applies to both your project's prompts AND your agent definitions:
- One good example teaches more than three paragraphs of rules
- When an agent needs to understand a pattern, show it, don't just describe it

---

## 8. Common Mistakes

| Mistake | Fix |
|---------|-----|
| Orchestrator writes code | Spawn an agent instead |
| Agent doesn't read tracker | Tracker protocol is the FIRST section in every agent .md |
| Agent doesn't update tracker | "When done (MANDATORY)" section with explicit steps |
| Team too large | Limit to 3-4 agents |
| No impact analysis | Always trace data flow before multi-file changes |
| Positive summary after failure | "Testing finds bugs, not proves success" |
| Same bug reintroduced | Add to Known Bugs table after every fix |
| Agent loads too much context | Keep agent .md under 150 lines |
| Orchestrator resolves disagreements silently | Surface all perspectives to the user |
| Work not recorded | Tracker + CHANGELOG update is mandatory, not optional |

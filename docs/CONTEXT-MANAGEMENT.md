# Context Window Management

How the multi-agent framework minimizes context usage and maximizes effective capacity.

---

## The Problem

Claude Code has a finite context window. Complex projects need:
- Full architecture understanding
- Deep domain knowledge
- Test patterns and edge cases
- Bug history and regressions
- UI component hierarchy
- API specifications

Loading all of this into a single context window leaves little room for actual work.

---

## The Solution: Distributed Context

### Layer 1: CLAUDE.md (Always Loaded)

**~200-400 lines.** Loaded on every session. Contains ONLY:
- Agent routing table (which agent handles what)
- Universal coding rules (all agents follow these)
- Known bugs table (prevents regressions)
- Naming conventions (prevents inconsistency)
- High-level dependency map (10-line overview)

**What CLAUDE.md does NOT contain:**
- Detailed architecture docs (that's in architect.md)
- Component hierarchy (that's in frontend.md)
- Database schema (that's in backend.md)
- Business rules (that's in domain-expert.md)

### Layer 2: Agent Definitions (~100-150 lines each)

Each agent loads its own `.md` file with domain-specific knowledge:
- Architecture details relevant to their domain
- Key file locations they need to know
- Conventions specific to their work
- Known issues in their domain

An agent NEVER loads another agent's definition. The frontend agent doesn't need to know database schema details.

### Layer 3: Trackers (~50-200 lines each)

Persistent state that agents read at session start:
- In-progress tasks to resume
- Blocked tasks and why
- Completed work (one-line summaries)

This is how work survives context resets without loading the full history.

### Layer 4: CHANGELOG (Append-Only)

Compressed record of all completed work:
- One-line summaries with date, files, and verification
- Anyone can scan it to understand what changed recently
- Prevents duplicate work across sessions

---

## Context Budget Math

| Component | Lines | Purpose |
|-----------|-------|---------|
| CLAUDE.md | ~300 | Routing + universal rules |
| Agent .md | ~120 | Domain expertise |
| Tracker .md | ~50 | Persistent state |
| CHANGELOG (recent) | ~50 | Recent history |
| **Total overhead** | **~520** | Before any work begins |

Compare to loading everything into one context:
- Full architecture: ~500 lines
- All domain knowledge: ~600 lines
- All test patterns: ~300 lines
- All bug history: ~200 lines
- **Total: ~1600 lines** just for context, in a single session

The multi-agent approach uses ~520 lines of overhead per agent, but each agent only needs its own 520 lines -- not everyone else's. The net savings grow with project complexity.

---

## Strategies

### 1. Progressive Disclosure

Don't put information in CLAUDE.md that agents can discover:

**BAD (in CLAUDE.md):**
```markdown
The UserProfile component has 15 props: name, email, avatar, ...
```

**GOOD (in CLAUDE.md):**
```markdown
User profile: `src/components/UserProfile.jsx`
```

The agent reads the file when it needs the details.

### 2. Return Clean Summaries

When agents return results, they provide summaries, not raw exploration:

**BAD agent return:**
```
I read 15 files, found that line 42 has a typo, also noticed line 89
could be optimized, and the CSS on line 12 uses an old pattern...
```

**GOOD agent return:**
```
Fixed: `user_service.py:42` -- `user.age` should be `user.date_of_birth`
(StudentProfile has no `age` field). Verified: py_compile PASS.
```

### 3. Tracker Compression

Completed tasks are compressed into one-line summaries. The full details lived in the agent's context during execution but don't need to persist:

**During execution:** Agent reads 20 files, traces 5 call chains, tries 3 approaches.
**In tracker:** `- **2026-01-15**: Fixed mastery calculation using display_mastery. Files: tracker.py, planner.py. Verified: E2E test PASS.`

### 4. Parallel Over Sequential

Three agents running in parallel use 3x the context budget but finish in 1/3 the time. The orchestrator's context only grows by the size of their return summaries.

### 5. Cost-Optimized Model Selection

Not every agent needs the most powerful model:

| Task Type | Recommended Model | Why |
|-----------|------------------|-----|
| Architecture analysis | Opus/Sonnet | Needs deep reasoning |
| Code review | Sonnet | Good pattern matching |
| Simple bug fix | Sonnet/Haiku | Straightforward task |
| File search / exploration | Haiku | Fast, cheap, read-only |
| Test execution | Sonnet | Needs to interpret results |

Use the `model` parameter in the Task tool: `model: "haiku"` for cheaper/faster tasks.

---

## When Context Gets Tight

If you're hitting context limits within a single session:

1. **Compress completed work** into tracker entries
2. **Spawn sub-agents** for investigation tasks (their context is separate)
3. **Split large tasks** into smaller increments across sessions
4. **Use Explore agents** for read-only research (returns clean summaries)
5. **Avoid loading unnecessary files** -- read on demand, not up front

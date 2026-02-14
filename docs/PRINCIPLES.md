# Core Principles

The engineering philosophy behind this framework. Heavily influenced by [Andrej Karpathy's observations](https://karpathy.bearblog.dev/) on AI-assisted coding and agentic engineering, battle-tested in production.

---

## 1. LLMs Don't Have Taste -- You Must Supply It

LLMs will write working code. They won't write *elegant* code. They overcomplicate, over-abstract, and over-engineer by default. They don't know when to stop.

**Your job is to resist.**

- They'll add a factory pattern for a single class
- They'll add error handling for cases that can never happen
- They'll build an abstraction the first time they see two similar lines
- They'll add "flexibility" and "configurability" you didn't ask for

**The test**: *"Would a senior engineer say this is overcomplicated?"*

If 200 lines could be 50, rewrite it. Three similar lines of code is better than a premature abstraction.

---

## 2. Success Criteria, Not Step-by-Step Instructions

LLMs are exceptionally good at looping until they meet specific goals. Don't tell them *what to do* -- tell them *what "done" looks like*.

**Bad**: "Read the file, find the function, change the parameter, save the file"
**Good**: "The function `calculate_total` should accept an optional `discount` parameter. When provided, it reduces the total. Tests in `test_calculate.py` should pass."

The second approach lets the LLM figure out HOW while you define WHAT. This is why goal-driven execution (write tests first, then make them pass) works so well with AI.

---

## 3. Plans and Specifications Before Prompting

Write design docs before implementation. Break work into well-defined tasks with clear acceptance criteria.

This isn't bureaucracy -- it's cost-effective AI management. A clear spec produces correct code on the first try. A vague request produces three rounds of revision.

**The paradox**: AI-assisted development actually rewards good engineering practices *more* than traditional coding does.
- Better specs -> better AI output
- Comprehensive tests -> confident delegation
- Clean architecture -> no hallucinated abstractions
- Clear naming -> fewer misunderstandings

---

## 4. Disciplined Review -- If You Can't Explain It, Don't Merge It

AI writes code fast. That's the easy part. The hard part is knowing whether the code is *right*.

- Review AI-generated code with the same rigor as human code
- If you can't explain why a fix works, it probably doesn't
- Workaround = BUG, not success
- Generic output = BROKEN (valid JSON does not equal correct behavior)
- Testing finds bugs, not proves success

**Karpathy's warning**: Junior developers risk skill atrophy by accepting AI output without understanding it. The framework's reviewer agent exists specifically to maintain review discipline.

---

## 5. Context Is Everything -- Fill the Window Right

LLMs perform dramatically better with the right context. Too little context = hallucinations. Wrong context = confident mistakes.

**What goes in CLAUDE.md** (~300 lines, loaded every session):
- Agent routing table
- Universal coding rules
- Known-bugs registry
- Naming conventions
- 10-line dependency map

**What goes in agent definitions** (~120 lines each, loaded per-agent):
- Domain-specific architecture
- Key file locations
- Domain conventions
- Domain-specific known bugs

**What does NOT go in CLAUDE.md**:
- Full architecture documentation (put in architect.md)
- Component hierarchies (put in frontend.md)
- Database schemas (put in backend.md)
- Business rules (put in domain-expert.md)

**Progressive disclosure**: Tell Claude *how to find* information rather than embedding it all. "User profile model is in `src/models/user.py`" beats pasting the entire model definition.

---

## 6. They Assume Wrong and Run With It

LLMs won't pause to verify a field name. They'll guess `user.name`, build three layers of logic on top of it, and you'll discover three hours later that the field is actually called `user.full_name`.

**The Verify Before Writing protocol exists for this reason:**
1. Read the source file -- confirm exact signatures, field names, return types
2. Check types at boundaries -- caller vs callee, Optional vs required
3. Grep before creating -- the function may already exist
4. Trace the full call chain -- a change at one layer ripples through all layers

**Code placement communicates specifications more efficiently than text descriptions.** Putting code in the right file/layer/module matters more than comments explaining why it's in the wrong place.

---

## 7. They Accumulate Instead of Consolidating

LLMs add new instructions alongside old ones instead of revising. You end up with:

```
Rule 1: "Always validate input"
Rule 2: "But skip validation for admin users"
Rule 3: "Actually, validate admin users too, but with different rules"
Rule 4: "Exception: super-admins skip validation entirely"
```

**The consolidation principle**: If you're adding a rule, check if an existing rule covers it. Revise the existing one, don't append a new one.

This applies to:
- Code (revise the function, don't add a wrapper)
- Prompts (update the existing instruction, don't add a contradicting one)
- Configuration (modify the existing config, don't add an override layer)
- Documentation (update the docs, don't add a "NEW:" section)

---

## 8. Examples Teach Better Than Rules

This is one of the most important principles for working with LLMs, both in prompts and in agent instructions.

**Abstract rule**: "Write clear, concise error messages"
**Example**:
```
BAD: "Error occurred"
BAD: "Invalid input: the provided value does not conform to the expected format"
GOOD: "Email must include @ symbol"
GOOD: "Password must be at least 8 characters"
```

The examples communicate more in 4 lines than the abstract rule does in 10 paragraphs.

**Application**: When writing agent definitions, include concrete examples of good/bad behavior. When writing prompts, include example inputs and expected outputs. When writing review checklists, include example violations.

---

## 9. The Known-Bugs Registry Is an Immune System

Every bug that takes >1 hour to fix gets documented with a prevention rule. This creates an immune system that learns from past infections.

**Why this matters more with AI**: LLMs don't have memory across sessions. Without the registry, the same bug gets reintroduced over and over. The registry makes prevention explicit and checkable.

**Pattern**:
```
| Bug | Rule |
|-----|------|
| user.age crash | UserProfile has no age field, use user.date_of_birth |
| SQL injection in search | Always use parameterized queries |
| N+1 query in user list | Always use select_related for user queries |
```

The reviewer agent checks this list on every code review. No exceptions.

---

## 10. The Orchestrator Sees the Surface -- Agents Find the Root Cause

This is the most counterintuitive principle. When a user reports a bug, the orchestrator's first instinct is to read the code, understand the problem, and propose a fix. **This is almost always wrong.**

**Why**: The orchestrator has broad but shallow knowledge. It sees the symptom ("data is stale") but not the root cause ("cache read happens before DB write"). Domain agents have deep knowledge of their layer and can trace the actual failure chain.

**The protocol**:
1. User reports problem
2. Orchestrator spawns investigation agents (architect + relevant domain agents) in parallel
3. Each agent investigates from their domain perspective
4. Orchestrator synthesizes findings
5. The root cause is usually different from (and deeper than) the surface symptom

**Example**: User says "tutor repeats questions." Surface analysis suggests a prompt fix. Domain expert finds the mastery pipeline has a bug causing the planner to select the same concept repeatedly. Architect finds the planner's routing table doesn't handle the edge case. The real fix is in the pipeline, not the prompt.

---

## 11. Persistent State Survives Context Drift

LLMs forget the beginning of a conversation as it gets longer. They lose track of what was decided, what was tried, and what failed.

**The framework's solution**: Persistent state in tracker files.
- Each agent reads its tracker at session start
- Each agent updates its tracker after completing work
- The CHANGELOG provides a global audit trail
- Decisions, rationale, and results survive across sessions

**Without persistent state**: Every new session starts from scratch, repeats investigations, and potentially reintroduces bugs. With persistent state: work compounds, decisions stick, and regressions are prevented.

---

## 12. Fail-Safe Degradation -- External Failures Must Not Cascade

When a third-party API goes down, your application should not:
- Crash
- Force-logout all users
- Show raw error messages
- Lose data silently

It SHOULD:
- Log the error
- Degrade gracefully (cached data, text-only mode, queued retry)
- Continue operating in reduced capacity
- Inform the user only if their action is affected

**The cascade principle**: A failure in an optional external system should never cascade into a failure of the core system. Design boundaries accordingly.

---

## Summary

| # | Principle | One-Line |
|---|-----------|----------|
| 1 | LLMs lack taste | You must actively resist over-engineering |
| 2 | Success criteria over steps | Tell it what "done" looks like, not how to get there |
| 3 | Specs before prompting | Better specs = better AI output |
| 4 | Disciplined review | If you can't explain it, don't merge it |
| 5 | Context is everything | Right info in the right place, progressive disclosure |
| 6 | They assume wrong | Verify before writing, always |
| 7 | Consolidate, don't accumulate | Revise existing rules, don't add patches |
| 8 | Examples > rules | One good/bad pair teaches more than paragraphs |
| 9 | Known-bugs as immune system | Every expensive bug gets a prevention rule |
| 10 | Orchestrator sees surface | Domain agents find root causes |
| 11 | Persistent state | Trackers survive context drift |
| 12 | Fail-safe degradation | External failures don't cascade |

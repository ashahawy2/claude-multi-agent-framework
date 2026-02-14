# Example: Single-Agent Task

## Scenario
User says: "Fix the CSS overlap on the dashboard sidebar"

## Orchestrator Routing

The orchestrator reads the request and matches keywords:
- "CSS" -> frontend
- "sidebar" -> frontend
- Single domain -> spawn ONE agent via Task tool

## What Happens

```
1. Orchestrator spawns frontend agent:
   Task(
     subagent_type: "general-purpose",
     prompt: "Fix the CSS overlap on the dashboard sidebar.
              Read .claude/agents/frontend.md for your instructions.
              Read .claude/trackers/frontend-tracker.md first.",
     description: "Fix sidebar CSS overlap"
   )

2. Frontend agent:
   a. Reads .claude/trackers/frontend-tracker.md (check for in-progress tasks)
   b. Reads the sidebar CSS file
   c. Identifies the overlap issue
   d. Makes minimal CSS fix
   e. Updates tracker: "- **2026-01-15**: Fixed sidebar overlap. Files: sidebar.css. Verified: visual inspection."
   f. Appends to .claude/CHANGELOG.md
   g. Returns summary to orchestrator

3. Orchestrator reports to user:
   "Fixed the sidebar CSS overlap. The issue was a missing `overflow: hidden`
    on `.dashboard-sidebar`. Change is in `src/styles/sidebar.css`."
```

## Key Points

- Orchestrator NEVER reads the CSS file itself
- Only ONE agent is spawned (no team overhead for a single-domain task)
- Agent updates tracker and CHANGELOG before returning
- Orchestrator returns a clean summary

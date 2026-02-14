# Example: Bug Investigation with Parallel Agents

## Scenario
User says: "Users are seeing stale data after updating their profile"

## Orchestrator Routing

The orchestrator reads the request:
- "stale data" -> could be frontend caching, backend caching, or database issue
- Root cause unclear -> parallel investigation
- Multiple domains -> TeamCreate

## What Happens

```
1. Orchestrator creates team:
   TeamCreate("stale-data-investigation")

2. Orchestrator spawns 3 investigation agents IN PARALLEL:

   Task(backend, "Investigate: after profile update, users see stale data.
        Trace the update flow from API to DB. Check if the DB write succeeds.
        Check if caching is involved. Report findings.")

   Task(frontend, "Investigate: after profile update, users see stale data.
        Check how the frontend handles profile update responses.
        Does it update local state? Does it refetch? Report findings.")

   Task(architect, "Investigate: after profile update, users see stale data.
        Trace the full data flow: frontend submit -> API -> DB -> response -> UI update.
        Identify where stale data could come from. Report findings.")

3. Agents investigate IN PARALLEL (each in their own context):

   Backend agent finds:
   "The POST /api/profile endpoint updates the DB correctly (verified via SQL query).
    BUT the response returns the OLD profile data because it reads from a cache
    that isn't invalidated after the write. Cache TTL is 5 minutes."

   Frontend agent finds:
   "The frontend correctly updates local state with the API response data.
    If the API returns stale data, the UI will show stale data.
    No client-side caching issue."

   Architect agent finds:
   "Data flow: Frontend POST -> API -> Cache read (stale!) -> DB write -> Return cached.
    The cache read happens BEFORE the DB write in the API handler.
    Fix: either invalidate cache after write, or read from DB for the response."

4. Orchestrator synthesizes all three findings:
   "Root cause identified by all 3 agents:

    The POST /api/profile handler reads from cache BEFORE writing to DB,
    then returns the cached (stale) data as the response.

    - Backend found: cache not invalidated after write (5-min TTL)
    - Frontend confirmed: no client-side caching issue, it trusts the API response
    - Architect traced: cache read happens before DB write in the handler

    Proposed fix: invalidate the profile cache after the DB write,
    then return the freshly-written data from the DB.

    Should I proceed with the fix?"

5. User approves. Orchestrator creates fix team:

   TaskCreate("Fix profile cache invalidation") → backend
   TaskCreate("E2E test profile update shows fresh data") → qa (blockedBy: [fix])
   TaskCreate("Review cache invalidation fix") → reviewer (blockedBy: [test])
```

## Key Insights

- **Three agents found the same root cause from different angles.** This builds confidence that we have the RIGHT root cause.
- **The frontend agent's "no issue found" was valuable.** It eliminated a hypothesis.
- **The architect traced the full flow** and identified WHERE in the flow the bug occurs (cache read before DB write).
- **No code was written during investigation.** First understand, then fix.

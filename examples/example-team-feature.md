# Example: Team Feature Implementation

## Scenario
User says: "Add a user search feature with API endpoint and UI"

## Orchestrator Routing

The orchestrator reads the request and matches keywords:
- "API endpoint" -> backend
- "UI" -> frontend
- Multiple domains -> TeamCreate

## What Happens

```
1. Orchestrator creates team:
   TeamCreate("user-search")

2. Orchestrator creates tasks with dependencies:
   TaskCreate("Design search API schema") → assign to architect
   TaskCreate("Implement /api/users/search endpoint") → assign to backend (blockedBy: [1])
   TaskCreate("Build SearchBar and SearchResults components") → assign to frontend (blockedBy: [2])
   TaskCreate("E2E test search feature") → assign to qa (blockedBy: [3])
   TaskCreate("Review all search feature changes") → assign to reviewer (blockedBy: [4])

3. Architect agent:
   a. Reads tracker, starts task
   b. Proposes: GET /api/users/search?q=...&page=1&limit=20
   c. Returns: { query: string, filters: object, pagination: object }
   d. Updates tracker, appends CHANGELOG
   e. Sends message to backend: "Schema ready, see task notes"

4. Backend agent (unblocked after architect completes):
   a. Reads tracker
   b. Implements search endpoint per architect's schema
   c. Adds query parameter validation
   d. Tests with curl
   e. Updates tracker, appends CHANGELOG
   f. Sends message to frontend: "API ready at /api/users/search"

5. Frontend agent (unblocked after backend completes):
   a. Reads tracker
   b. Builds SearchBar with debounced input
   c. Builds SearchResults with pagination
   d. Integrates with backend API
   e. Updates tracker, appends CHANGELOG

6. QA agent (unblocked after frontend completes):
   a. Reads tracker
   b. Tests: search with results, empty search, special characters, pagination
   c. Reports: 4/5 PASS, 1 FAIL (special characters not escaped)
   d. Creates follow-up task for backend: "Escape special chars in search query"
   e. Updates tracker, appends CHANGELOG

7. Reviewer agent (unblocked after QA completes):
   a. Reads all changed files
   b. Runs through review checklist
   c. Reports: APPROVED WITH SUGGESTIONS (add index on search column)
   d. Updates tracker, appends CHANGELOG

8. Orchestrator synthesizes:
   "Search feature implemented:
    - API: GET /api/users/search with query, filters, pagination
    - UI: SearchBar + SearchResults components
    - QA: 4/5 tests pass (1 bug filed for special char escaping)
    - Review: Approved, suggestion to add DB index
    Files: user_routes.py, SearchBar.jsx, SearchResults.jsx, search.css"
```

## CHANGELOG After Completion

```markdown
## 2026-01-15

### Architect -- Search API schema design (architect agent)
- **2026-01-15**: Designed GET /api/users/search with query/filter/pagination params.
  Files: (advisory, no code changes). Verified: team consensus.

### Backend -- Search endpoint implementation (backend agent)
- **2026-01-15**: Implemented /api/users/search with full-text search, pagination,
  and input validation. Files: user_routes.py, user_service.py, user_repository.py.
  Verified: curl tests PASS.

### Frontend -- Search UI components (frontend agent)
- **2026-01-15**: Built SearchBar (debounced input) and SearchResults (paginated list).
  Files: SearchBar.jsx, SearchResults.jsx, search.css. Verified: visual inspection.

### QA -- Search feature E2E tests (qa agent)
- **2026-01-15**: 4/5 tests PASS. FAIL: special characters in search query not escaped.
  Bug filed for backend. Verified: browser automation.

### Reviewer -- Search feature code review (reviewer agent)
- **2026-01-15**: APPROVED WITH SUGGESTIONS. Suggestion: add index on users.name for
  search performance. Files reviewed: 5. Verified: checklist review.
```

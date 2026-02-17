# Project Reference Material

Agents: read this file when you need naming conventions, known bugs, existing features, or architecture context.

## Naming Conventions

> **CUSTOMIZE** with your project's naming conventions.
> Naming conventions are contracts, not style preferences. Using a different name for
> an established concept is a bug.

| Context | Correct | Wrong |
|---------|---------|-------|
| _Database columns_ | _`snake_case`_ | _`camelCase`_ |
| _API endpoints_ | _`kebab-case`_ | _`snake_case`_ |
| _React components_ | _`PascalCase`_ | _`camelCase`_ |
| _CSS classes_ | _`kebab-case`_ | _`camelCase`_ |
| _Environment variables_ | _`SCREAMING_SNAKE`_ | _`camelCase`_ |
| _Constants_ | _`SCREAMING_SNAKE`_ | _`camelCase`_ |

## Fixed Bugs -- Do NOT Reintroduce

> **Every bug that takes >1 hour to fix gets added here.**
> Every agent and the reviewer check this list before making changes.
> This is the project's immune system -- it learns from past infections.

| Bug | Rule |
|-----|------|
| _Example: `user.age` crash_ | _`UserProfile` has no `age` field, use `user.date_of_birth`_ |
| _Example: SQL injection in search_ | _Always use parameterized queries, never string interpolation_ |
| _Example: N+1 query in user list_ | _Always use `select_related` / `prefetch_related` for user queries_ |

## Existing Features -- Do NOT Reimplement

> **Grep before creating.** If you're about to write a utility function, search first.
> Duplicating existing code is worse than finding it.

| Feature | Location |
|---------|----------|
| _Example: Authentication_ | _`src/auth/`_ |
| _Example: Email service_ | _`src/services/email.py`_ |
| _Example: Date formatting_ | _`src/utils/dates.py`_ |

## High-Level Dependency Map

> **CUSTOMIZE** with your project's architecture.
> Verify against actual imports before trusting this. Architect agent owns keeping this current.

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

## Fail-Safe Degradation

When external services fail, the application MUST degrade gracefully:

| External Failure | Response | NEVER Do |
|-----------------|----------|----------|
| Third-party API timeout | Return cached/fallback data, log error | Crash the request or show raw error to user |
| Auth provider down | Use cached session, extend token TTL | Force logout all users |
| File storage unavailable | Queue upload for retry, show placeholder | Lose the upload silently |
| LLM rate limited | Queue request, show loading state | Return empty/garbage response |

**Rule**: External failures MUST NOT cascade to user-facing errors. Log, degrade, continue.

## Prompt Engineering Rules (For LLM-Integrated Projects)

> Skip this section if your project doesn't use LLM prompts.

- **Do NOT remove calibration scores.** Numeric thresholds are precision tools, not clutter.
- **Describe intent, not cases.** Give the LLM principles, not if-else branches.
- **One clear instruction beats three overlapping ones.** Audit for contradictions.
- **Consolidate, don't accumulate.** Revise existing instructions, don't append patches.
- **Examples > rules.** One good/bad example pair teaches more than three paragraphs.
- **Keep prompts DRY.** Same instruction in 4 places = extract a shared section.
- **Test prompts empirically.** Generate 2-3 responses and check.
- **Strong directives work.** `MUST`, `NEVER`, `CRITICAL` + examples > `should`, `try to`, `consider`.
- **Prompt changes MUST preserve contracts** -- see `.claude/prompt-contracts.md`.

## LLM-Specific Awareness

LLMs (including the agents you spawn) have known failure modes. Guard against them:

- **They overcomplicate.** They'll add abstractions, error handling, and "flexibility" you didn't ask for. Actively resist.
- **They don't clean up.** Dead imports, unused variables, orphaned functions -- they won't notice. You must.
- **They assume wrong and run with it.** They won't pause to verify a field name -- they'll guess and build on the guess.
- **They accumulate instead of consolidating.** They'll add new rules alongside old ones instead of revising.
- **Examples teach better than rules.** One concrete example of good/bad behavior is worth three paragraphs of abstract guidelines.
- **They lose context.** The further a conversation goes, the more they forget the beginning. This is why trackers and changelogs exist.

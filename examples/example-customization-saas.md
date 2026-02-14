# Example: Customizing for a SaaS Project

How to adapt the framework for a typical SaaS application.

## Project Context
- **Stack**: Next.js frontend, Django backend, PostgreSQL, Redis, Stripe
- **Domain**: Project management tool with team collaboration

---

## CLAUDE.md Customization

### Agent Roster
```markdown
| Agent | File | Domain |
|-------|------|--------|
| **architect** | `.claude/agents/architect.md` | System design, API contracts, data flow |
| **frontend** | `.claude/agents/frontend.md` | Next.js pages, React components, Tailwind |
| **backend** | `.claude/agents/backend.md` | Django views, DRF serializers, Celery tasks |
| **domain-expert** | `.claude/agents/domain-expert.md` | Billing rules, permissions, team logic |
| **reviewer** | `.claude/agents/reviewer.md` | Code review, security, regression checking |
| **qa** | `.claude/agents/qa.md` | E2E with Playwright, API testing |
```

### Auto-Routing
```markdown
| If the task involves... | Route to |
|------------------------|----------|
| Next.js, React, Tailwind, components, pages, layout | **frontend** |
| Django, DRF, serializers, views, Celery, PostgreSQL | **backend** |
| Billing, Stripe, subscriptions, permissions, team roles | **domain-expert** |
| API contracts, data flow, schema changes, migrations | **architect** |
| Code review, PR review, security audit | **reviewer** |
| E2E testing, Playwright, regression testing | **qa** |
```

### Known Bugs
```markdown
| Bug | Rule |
|-----|------|
| Team invite race condition | Use `select_for_update()` on team member count |
| Stripe webhook duplicate processing | Always check idempotency key before processing |
| N+1 query in project list | Use `select_related('owner', 'team')` |
| CORS error on file upload | Ensure `Content-Type` header is not set for multipart |
```

### Naming Conventions
```markdown
| Domain | Convention | Example |
|--------|-----------|---------|
| Django models | PascalCase | `ProjectMember`, `TeamInvite` |
| API endpoints | kebab-case | `/api/v1/team-invites` |
| React components | PascalCase | `ProjectBoard`, `TeamSettings` |
| Tailwind classes | kebab-case | `bg-primary`, `text-sm` |
| Celery tasks | snake_case | `send_invite_email`, `sync_stripe` |
| DB tables | snake_case plural | `projects`, `team_members` |
```

---

## Domain Expert Customization

The domain-expert agent for this SaaS would include:

```markdown
## Business Rules

### Billing
- Free tier: 3 projects, 5 team members
- Pro tier: unlimited projects, 25 team members
- Enterprise: unlimited everything
- Downgrade: projects/members over limit become read-only, NOT deleted
- Trial: 14 days, full Pro features

### Permissions
| Role | Create Project | Invite Member | Manage Billing | Delete Team |
|------|---------------|---------------|----------------|-------------|
| Owner | Yes | Yes | Yes | Yes |
| Admin | Yes | Yes | No | No |
| Member | Yes | No | No | No |
| Guest | No | No | No | No |

### Team Invite Flow
draft -> sent -> accepted -> active
draft -> sent -> declined -> (deleted)
draft -> sent -> expired (7 days) -> (deleted)

### Stripe Integration
- Subscription changes take effect immediately
- Prorated charges for mid-cycle upgrades
- Grace period: 3 failed payments before suspension
- Webhook events: checkout.session.completed, invoice.paid, invoice.payment_failed
```

---

## Why This Works

1. **Backend agent** knows Django patterns, DRF serializers, Celery best practices
2. **Frontend agent** knows Next.js routing, React patterns, Tailwind conventions
3. **Domain expert** knows billing rules, permission matrices, invite flows
4. **Architect** traces API contracts between frontend and backend
5. **Reviewer** catches N+1 queries, missing permissions checks, Stripe webhook bugs
6. **QA** tests full user journeys: signup -> create team -> invite member -> start project

Each agent carries ~120 lines of domain knowledge. No single context window needs to hold everything.

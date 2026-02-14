# Setup Guide

Step-by-step instructions for adopting the multi-agent framework in your project.

---

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- A project with clear domain boundaries (frontend/backend/etc.)

---

## Step 1: Copy the Framework

Copy the `.claude/` directory and `CLAUDE.md` into your project root:

```bash
cp -r claude-multi-agent-framework/.claude your-project/.claude
cp claude-multi-agent-framework/CLAUDE.md your-project/CLAUDE.md
```

## Step 2: Enable Agent Teams

Add to your Claude Code settings. Either globally (`~/.claude/settings.json`) or per-project (`.claude/settings.local.json`):

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Step 3: Customize CLAUDE.md

Edit `CLAUDE.md` to reflect YOUR project:

### 3a. Agent Roster
Keep the agents that match your project's domains. Remove ones you don't need.

**Minimum viable setup:** backend + frontend + reviewer (3 agents)
**Full setup:** all 6 agents

### 3b. Auto-Routing Table
Update the keywords that trigger each agent. Add domain-specific terms:

```markdown
| If the task involves... | Route to |
|------------------------|----------|
| React, Next.js, Tailwind, components | **frontend** |
| Django, PostgreSQL, API, Celery | **backend** |
| Payment rules, subscription logic | **domain-expert** |
```

### 3c. Naming Conventions
Document YOUR project's naming patterns:

```markdown
| Domain | Convention | Example |
|--------|-----------|---------|
| Models | PascalCase | `UserProfile`, `OrderItem` |
| API | kebab-case | `/api/user-profiles` |
| DB | snake_case | `user_profiles`, `created_at` |
```

### 3d. Known Bugs
Start with an empty table. Add bugs as you fix them:

```markdown
| Bug | Rule |
|-----|------|
| N+1 query in user list | Always use `select_related` for user queries |
```

### 3e. Dependency Map
Sketch your architecture in 10-15 lines:

```markdown
Frontend (Next.js) --> API (Django REST)
  --> Services (business logic)
    --> Models (Django ORM)
      --> PostgreSQL
```

## Step 4: Customize Agent Definitions

Edit each agent file in `.claude/agents/`. For each agent:

### 4a. Service Architecture
Replace the template sections with YOUR project's actual architecture:

```markdown
### Services and Their Roles
| Service | File | Purpose |
|---------|------|---------|
| UserService | `src/services/user.py` | User CRUD, profile management |
| PaymentService | `src/services/payment.py` | Stripe integration, billing |
```

### 4b. Key Files
List the files each agent needs to know about:

```markdown
## Key Files
- API routes: `src/api/routes/`
- Services: `src/services/`
- Models: `src/models/`
- Tests: `tests/`
```

### 4c. Domain Knowledge
Add the specialized knowledge each agent needs. The backend agent needs database schema; the frontend agent needs component hierarchy; the domain expert needs business rules.

## Step 5: Commit to Version Control

All files in `.claude/` should be committed to git:

```bash
git add .claude/ CLAUDE.md
git commit -m "Add multi-agent framework for Claude Code"
```

This means:
- Team members share the same agent definitions
- Agent knowledge evolves with the codebase
- Trackers persist across sessions via git

## Step 6: Start Using It

Open Claude Code in your project. The orchestrator (CLAUDE.md) loads automatically.

**Try it:**
- "Fix the login form validation" -> routes to frontend agent
- "Add a /api/users endpoint" -> routes to backend agent
- "Review the recent changes" -> routes to reviewer agent
- "Add user search with UI and API" -> creates a team

---

## Removing Agents You Don't Need

If your project doesn't need all 6 agents:

1. Delete the agent `.md` file from `.claude/agents/`
2. Delete its tracker from `.claude/trackers/`
3. Remove it from the agent roster in `CLAUDE.md`
4. Remove its routing entries from the auto-routing table

**Common 3-agent setup:** backend + frontend + reviewer
**Common 4-agent setup:** backend + frontend + qa + reviewer

---

## Adding Custom Agents

To add a new specialist agent:

1. Create `.claude/agents/your-agent.md` following the agent template
2. Create `.claude/trackers/your-agent-tracker.md` following the tracker template
3. Add it to the agent roster in `CLAUDE.md`
4. Add routing entries for it in the auto-routing table

**Example custom agents:**
- **devops** -- CI/CD, Docker, Kubernetes, infrastructure
- **security** -- Auth, permissions, vulnerability scanning
- **data** -- Migrations, ETL, data quality, analytics
- **mobile** -- iOS/Android, React Native, Flutter

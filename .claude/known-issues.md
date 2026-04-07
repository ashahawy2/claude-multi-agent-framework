# Known Issues Registry

Quality issues discovered through audits, testing, or production use. Every agent checks this registry before modifying artifacts.

## How to Use

- **Before modifying an artifact:** Check if any KI entries reference it
- **After discovering a quality issue:** Add a KI entry here
- **After fixing a KI issue:** Update status to `resolved` with date and fix reference

## Registry

| ID | Severity | Description | Affected Artifacts | Prevention Rule | Status |
|----|----------|-------------|-------------------|-----------------|--------|
| _KI-001_ | _Critical_ | _Example: Agent skips validation step_ | _`src/validators/`_ | _Always validate before processing_ | _open_ |

> Start empty. Add entries as you discover quality issues.

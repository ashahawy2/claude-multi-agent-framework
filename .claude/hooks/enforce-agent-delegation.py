#!/usr/bin/env python3
"""
PreToolUse hook: Prevents the orchestrator from editing source code files.

The orchestrator's job is routing, coordination, and synthesis -- not writing code.
This hook enforces that discipline by blocking Edit/Write tool calls on source code
files. Only specialist agents (spawned via Task tool) should modify code.

The orchestrator CAN still edit:
  - .md files (trackers, changelogs, documentation)
  - .json config files in .claude/ (settings, etc.)

How it works:
  - Claude Code invokes this script as a PreToolUse hook for Edit and Write tools
  - The script receives a JSON payload on stdin with tool_name and tool_input
  - If the target file is a source code file, the script exits with code 2 (block)
  - If the target file is allowed (.md, .claude/ config), the script exits with code 0 (allow)

Setup:
  Add to .claude/settings.local.json under "hooks":

  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "python .claude/hooks/enforce-agent-delegation.py"
      }
    ]
  }
"""

import json
import os
import sys


# Source code extensions that the orchestrator must NOT edit directly.
# Customize this list for your project's tech stack.
SOURCE_CODE_EXTENSIONS = {
    # Python
    ".py",
    # JavaScript / TypeScript
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    # Web
    ".html", ".css", ".scss", ".sass", ".less",
    # Backend
    ".java", ".kt", ".go", ".rs", ".rb", ".php",
    # Mobile
    ".swift", ".m", ".dart",
    # Config that affects runtime behavior
    ".yaml", ".yml", ".toml",
    # C/C++
    ".c", ".cpp", ".h", ".hpp",
    # Shell
    ".sh", ".bash", ".zsh",
    # SQL
    ".sql",
}

# Files/directories the orchestrator IS allowed to edit.
# These are coordination files, not source code.
ALLOWED_PATTERNS = [
    ".md",           # Markdown (trackers, changelogs, docs)
    ".claude/",      # Claude config directory
    "CLAUDE.md",     # Orchestrator instructions
]


def is_allowed_file(file_path: str) -> bool:
    """Check if the orchestrator is allowed to edit this file."""
    if not file_path:
        return True  # No file path = allow (tool may not need one)

    # Normalize path separators
    normalized = file_path.replace("\\", "/")

    # Allow .md files (trackers, changelogs, documentation)
    if normalized.endswith(".md"):
        return True

    # Allow files inside .claude/ directory (settings, hooks, etc.)
    if "/.claude/" in normalized or normalized.startswith(".claude/"):
        return True

    # Block source code files
    _, ext = os.path.splitext(normalized)
    if ext.lower() in SOURCE_CODE_EXTENSIONS:
        return False

    # Default: allow unknown extensions (be permissive for non-code files)
    return True


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        # If we can't parse input, allow the operation (fail-open)
        sys.exit(0)

    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not is_allowed_file(file_path):
        # Exit code 2 = block the tool call. Stderr message is shown to Claude.
        print(
            f"BLOCKED: Orchestrator cannot edit source code files directly. "
            f"Delegate to a specialist agent instead.\n"
            f"  File: {file_path}\n"
            f"  Rule: The orchestrator routes tasks and synthesizes results. "
            f"Only specialist agents (frontend, backend, domain-expert, etc.) write code.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Exit code 0 = allow
    sys.exit(0)


if __name__ == "__main__":
    main()

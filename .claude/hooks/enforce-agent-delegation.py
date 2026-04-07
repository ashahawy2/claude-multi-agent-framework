#!/usr/bin/env python3
"""Agent-identity-aware PreToolUse hook. Exit 0=allow, 2=block."""

import json, os, re, sys

SOURCE_CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".html", ".css", ".scss", ".sass", ".less",
    ".java", ".kt", ".go", ".rs", ".rb", ".php",
    ".swift", ".m", ".dart", ".yaml", ".yml", ".toml",
    ".c", ".cpp", ".h", ".hpp", ".sh", ".bash", ".zsh", ".sql",
}

# CUSTOMIZE: Map agents to directories they can edit
AGENT_DOMAIN_MAP = {
    "frontend": {"src/components/", "src/styles/", "src/ui/", "src/pages/", "src/views/"},
    "backend": {"src/api/", "src/services/", "src/models/", "src/database/", "src/middleware/"},
    "domain-expert": {"src/domain/", "src/rules/", "src/config/", "src/validators/"},
    "architect": set(),
    "qa": {"tests/", "e2e/", "cypress/", "__tests__/"},
}

def is_safe(fp):
    if not fp: return True
    n = fp.replace("\\", "/")
    return n.endswith(".md") or "/.claude/" in n or n.startswith(".claude/")

def is_source(fp):
    if not fp: return False
    _, ext = os.path.splitext(fp)
    return ext.lower() in SOURCE_CODE_EXTENSIONS

def detect_agent(conv):
    pat = re.compile(r"You are the \\*{0,2}(\\w[\\w-]*)\\*{0,2} agent")
    for msg in conv:
        if not isinstance(msg, dict): continue
        c = msg.get("content", "")
        texts = [c] if isinstance(c, str) else [b.get("text","") if isinstance(b,dict) else str(b) for b in c if b]
        for t in texts:
            m = pat.search(t)
            if m: return m.group(1).lower()
    return None

def has_override(conv):
    for msg in conv:
        if not isinstance(msg, dict) or msg.get("role") != "user": continue
        c = msg.get("content", "")
        if isinstance(c, str) and "#direct-edit" in c: return True
        if isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and "#direct-edit" in b.get("text", ""): return True
    return False

def can_edit(name, fp):
    if name not in AGENT_DOMAIN_MAP: return True
    dirs = AGENT_DOMAIN_MAP[name]
    if not dirs: return False
    n = fp.replace("\\", "/")
    return any(d in n for d in dirs)

def main():
    try: payload = json.load(sys.stdin)
    except: sys.exit(0)
    fp = payload.get("tool_input", {}).get("file_path", "")
    if is_safe(fp): sys.exit(0)
    if "conversation" not in payload: sys.exit(0)
    if not is_source(fp): sys.exit(0)
    conv = payload.get("conversation", [])
    if has_override(conv): sys.exit(0)
    agent = detect_agent(conv)
    if agent and can_edit(agent, fp): sys.exit(0)
    r = f"The {agent} agent cannot edit {fp}." if agent else "Delegate to specialist agent."
    print(json.dumps({"decision":"block","reason":r+" User: #direct-edit to override."}), file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__": main()

"""Check every agent and skill file has a valid header (frontmatter).

Claude Code silently ignores misspelled or unknown header fields, so a typo
like `modle: haiku` would quietly run the agent on your most expensive model.
This script catches that.

Usage:
    python scripts/check_agents.py          # exit 1 if any problem is found
"""

import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AGENT_FIELDS = {
    "name", "description", "tools", "disallowedTools", "model", "effort", "permissionMode",
    "maxTurns", "autoCompactWindow", "skills", "mcpServers", "hooks", "memory", "background",
    "omitClaudeMd", "isolation", "initialPrompt", "experimental", "color",
}
SKILL_FIELDS = {
    "name", "description", "allowed-tools", "model", "disable-model-invocation",
    "user-invocable", "argument-hint", "license", "version", "metadata", "effort", "context", "agent",
}
MODELS = {"haiku", "sonnet", "opus", "fable", "inherit"}


def read_header(path):
    """Return the top-level keys of the YAML header as {key: value-string}."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    header = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return header
        if line and not line.startswith((" ", "\t", "#")) and ":" in line:
            key, value = line.split(":", 1)
            header[key.strip()] = value.strip()
    return None  # header never closed


def check(path, allowed, need_model):
    problems = []
    header = read_header(path)
    try:
        rel = os.path.relpath(path, ROOT)
    except ValueError:
        rel = path  # on Windows, a file on another drive (D: vs C:) has no relative path
    if header is None:
        return [f"{rel}: missing or unclosed --- header"]
    for key in ("name", "description"):
        if key not in header:
            problems.append(f"{rel}: missing '{key}'")
    for key in header:
        if key not in allowed:
            problems.append(f"{rel}: unknown field '{key}' (typo? Claude Code ignores it)")
    model = header.get("model")
    if need_model and not model:
        problems.append(f"{rel}: no 'model' set, so it would run on the parent (often most expensive) model")
    if model and model not in MODELS and not model.startswith("claude-"):
        problems.append(f"{rel}: unusual model '{model}'")
    return problems


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    problems = []
    agents = sorted(glob.glob(os.path.join(ROOT, ".claude", "agents", "*.md")))
    skills = sorted(glob.glob(os.path.join(ROOT, ".claude", "skills", "*", "SKILL.md")))
    for path in agents:
        problems += check(path, AGENT_FIELDS, need_model=True)
    for path in skills:
        problems += check(path, SKILL_FIELDS, need_model=False)
    for p in problems:
        print("PROBLEM:", p)
    print(f"Checked {len(agents)} agents and {len(skills)} skills: {len(problems)} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

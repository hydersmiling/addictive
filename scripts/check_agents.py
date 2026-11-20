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
    with open(path, encoding="utf-8-sig", errors="replace") as fh:  # -sig: tolerate a Windows BOM
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


# Limits from Anthropic's skills documentation (code.claude.com/docs/en/skills).
MAX_SKILL_LINES = 500          # a loaded SKILL.md stays in context every turn
MAX_LISTING_CHARS = 1536       # name + description, as shown in the skill listing


def check_limits(path):
    """Problems with a SKILL.md's size or listing text, per Anthropic's guidance."""
    rel = os.path.relpath(path, ROOT) if os.path.splitdrive(path)[0] == os.path.splitdrive(ROOT)[0] else path
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        lines = fh.read().splitlines()
    header = read_header(path) or {}
    found = []
    if len(lines) > MAX_SKILL_LINES:
        found.append(f"{rel}: {len(lines)} lines (limit {MAX_SKILL_LINES}); move detail into references/")
    listing = len(header.get("name", "")) + len(header.get("description", ""))
    if listing > MAX_LISTING_CHARS:
        found.append(f"{rel}: name + description is {listing} characters (limit {MAX_LISTING_CHARS})")
    return found


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    problems = []
    root = glob.escape(ROOT)  # a folder name with [ ] * ? must not break the search
    agents = sorted(glob.glob(os.path.join(root, "agents", "*.md")))
    agents += sorted(glob.glob(os.path.join(root, "optional", "agents-catalog", "*.md")))
    skills = sorted(glob.glob(os.path.join(root, ".claude", "skills", "*", "SKILL.md")))
    skills += sorted(glob.glob(os.path.join(root, "optional", "**", "SKILL.md"), recursive=True))
    if not agents or not skills:
        print("PROBLEM: no agent or skill files found; refusing to report a pass.")
        return 1
    for path in agents:
        problems += check(path, AGENT_FIELDS, need_model=True)
    warnings = []
    for path in skills:
        problems += check(path, SKILL_FIELDS, need_model=False)
        # Core skills must meet the limits; optional third-party skills only get a warning.
        if os.sep + "optional" + os.sep in path or "/optional/" in path:
            warnings += check_limits(path)
        else:
            problems += check_limits(path)
    for w in warnings:
        print("WARNING:", w)
    for p in problems:
        print("PROBLEM:", p)
    print(f"Checked {len(agents)} agents and {len(skills)} skills: {len(problems)} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

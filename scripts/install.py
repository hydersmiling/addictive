"""Copy the Mainseat kit into one of your projects.

Usage:
    python scripts/install.py PATH --dry-run                  # show what would happen
    python scripts/install.py PATH                            # install the core kit
    python scripts/install.py PATH --with dev-essentials      # plus optional skill packs
    python scripts/install.py --list-agents                   # show the 198 catalog agents
    python scripts/install.py PATH --agents security-auditor  # add catalog agents by name

Core kit: agents, skills, CLAUDE.md (from the template), .claude/settings.json,
.claude/LEARNED.md, and the map and token scripts.

Plugin users: the plugin provides agents and skills; /mainseat:setup runs this script with
--rules-only to add only the per-project files.

Optional packs (installed only when named with --with):
    code-graph      knowledge graph for large codebases (needs: uv tool install graphifyy)
    dev-essentials  debugging, code review, git, error handling, Python and JS testing
    llm-compress    for apps you build that call an LLM API (adds the headroom-ai package)

Agent catalog: 198 specialised subagents (optional/agents-catalog). Install only the
ones you need: every installed agent's description is loaded in every session.

It NEVER overwrites a file you already have. Existing files are skipped and listed.
"""

import argparse
import os
import shutil
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (source in the kit, destination in the project)
SINGLE_FILES = [
    ("scripts/make_codemap.py", "scripts/make_codemap.py"),
    ("scripts/measure_tokens.py", "scripts/measure_tokens.py"),
    ("CLAUDE.md.template", "CLAUDE.md"),
    (".claude/settings.json", ".claude/settings.json"),
    (".claude/LEARNED.md", ".claude/LEARNED.md"),
]
CORE_FOLDERS = [(".claude/agents", ".claude/agents"), (".claude/skills", ".claude/skills")]
OPTIONAL = {
    "code-graph": [("optional/code-graph", ".claude/skills/code-graph")],
    "dev-essentials": [("optional/dev-essentials", ".claude/skills")],
    "llm-compress": [("optional/llm-compress", ".claude/skills/llm-compress")],
}
CATALOG = os.path.join(KIT, "optional", "agents-catalog")


def catalog_agents():
    """Names of the agents in the optional catalog."""
    return sorted(f[:-3] for f in os.listdir(CATALOG) if f.endswith(".md"))


def walk_pairs(src_folder, dst_folder):
    """(source, destination) pairs for every file under src_folder."""
    pairs = []
    for dirpath, _dirs, files in os.walk(src_folder):
        for name in files:
            src = os.path.join(dirpath, name)
            pairs.append((src, os.path.join(dst_folder, os.path.relpath(src, src_folder))))
    return pairs


def plan(target, extras=(), agents=(), rules_only=False):
    """Return the sorted list of (source, destination) file pairs to copy."""
    pairs = [(os.path.join(KIT, s), os.path.join(target, d)) for s, d in SINGLE_FILES]
    for name in agents:
        pairs.append((os.path.join(CATALOG, name + ".md"),
                      os.path.join(target, ".claude", "agents", name + ".md")))
    # rules_only: the plugin already provides agents and skills, so copy only project files.
    folders = ([] if rules_only else CORE_FOLDERS) + [f for name in extras for f in OPTIONAL[name]]
    for src, dst in folders:
        pairs += walk_pairs(os.path.join(KIT, src), os.path.join(target, dst))
    return sorted(pairs)


def install(target, dry_run=False, extras=(), agents=(), rules_only=False):
    """Copy kit files into target. Return (copied, skipped) lists of relative paths."""
    copied, skipped = [], []
    for src, dst in plan(target, extras, agents, rules_only):
        rel = os.path.relpath(dst, target)
        if os.path.lexists(dst):  # lexists: also skip broken symlinks, never write through them
            skipped.append(rel)
            continue
        copied.append(rel)
        if not dry_run:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
    return copied, skipped


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Copy the Mainseat kit into a project.")
    parser.add_argument("target", nargs="?", help="your project folder")
    parser.add_argument("--dry-run", action="store_true", help="show what would be copied; change nothing")
    parser.add_argument("--with", dest="extras", nargs="+", default=[], choices=sorted(OPTIONAL),
                        help="optional packs to add")
    parser.add_argument("--agents", nargs="+", default=[], metavar="NAME",
                        help="catalog agents to add (see --list-agents)")
    parser.add_argument("--list-agents", action="store_true", help="list catalog agents and exit")
    parser.add_argument("--rules-only", action="store_true",
                        help="only CLAUDE.md, settings, LEARNED.md and scripts (for plugin installs)")
    args = parser.parse_args(argv)

    if args.list_agents:
        names = catalog_agents()
        print(f"{len(names)} catalog agents:")
        for name in names:
            print("  " + name)
        return 0
    if not args.target:
        parser.error("give your project folder")
    unknown = sorted(set(args.agents) - set(catalog_agents()))
    if unknown:
        print(f"Unknown catalog agents: {', '.join(unknown)}. See --list-agents.")
        return 1

    target = os.path.abspath(args.target)
    if not os.path.isdir(target):
        print(f"Not a folder: {target}")
        return 1
    if os.path.samefile(target, KIT):
        print("That is the kit itself. Pick your own project folder.")
        return 1

    copied, skipped = install(target, args.dry_run, args.extras, args.agents, args.rules_only)
    print(f"{'Would copy' if args.dry_run else 'Copied'} {len(copied)} files into {target}")
    for rel in copied:
        print(f"  + {rel}")
    if skipped:
        print(f"Skipped {len(skipped)} files you already have:")
        for rel in skipped:
            print(f"  = {rel}")
    if not args.dry_run:
        print("\nNext steps:")
        if "CLAUDE.md" in skipped:
            print(f"  1. Merge what you want from {os.path.join(KIT, 'CLAUDE.md.template')} into your CLAUDE.md.")
        else:
            print("  1. Fill in the 'Project' and 'Run tests' lines in CLAUDE.md.")
        print("  2. Run: python scripts/make_codemap.py")
        print("  3. Start Claude Code on Sonnet (recommended): claude --model sonnet")
        print("     Sonnet runs the session; Opus is called only through the planner agent.")
        print("     Measured: 44-56% cheaper than plain Opus with the same pass rate.")
        print("  4. No Fable access? Set 'model: opus' in .claude/agents/big-decision.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

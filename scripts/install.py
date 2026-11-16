"""Copy the Addictive kit into one of your projects.

Usage:
    python scripts/install.py C:\\path\\to\\your-project --dry-run   # show what would happen
    python scripts/install.py C:\\path\\to\\your-project             # do it
    python scripts/install.py C:\\path\\to\\your-project --with-code-graph   # plus the optional graph skill

What it copies:
  .claude/agents/*        subagents (scout, builder, reviewer, debugger, researcher, big-decision)
  .claude/skills/*        skills (terse, map, lean-code, reuse-first, self-check, ...)
  .claude/LEARNED.md      empty list of rules Claude learns from your corrections
  scripts/make_codemap.py and scripts/measure_tokens.py
  CLAUDE.md.template  ->  CLAUDE.md          (only if you have no CLAUDE.md)
  .claude/settings.json                       (only if you have none)

It NEVER overwrites a file you already have. Existing files are skipped and
listed, so you can merge them by hand.
"""

import argparse
import os
import shutil
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (source inside the kit, destination inside the project)
SINGLE_FILES = [
    ("scripts/make_codemap.py", "scripts/make_codemap.py"),
    ("scripts/measure_tokens.py", "scripts/measure_tokens.py"),
    ("CLAUDE.md.template", "CLAUDE.md"),
    (".claude/settings.json", ".claude/settings.json"),
    (".claude/LEARNED.md", ".claude/LEARNED.md"),
]
# Optional extras: (source folder in the kit, destination folder in the project)
OPTIONAL = {"code-graph": ("optional/code-graph", ".claude/skills/code-graph")}
FOLDERS = [".claude/agents", ".claude/skills"]


def walk_pairs(src_folder, dst_folder):
    """(source, destination) pairs for every file under src_folder."""
    pairs = []
    for dirpath, _dirs, files in os.walk(src_folder):
        for name in files:
            src = os.path.join(dirpath, name)
            pairs.append((src, os.path.join(dst_folder, os.path.relpath(src, src_folder))))
    return pairs


def plan(target, extras=()):
    """Return a list of (source, destination) file pairs to copy."""
    pairs = [(os.path.join(KIT, s), os.path.join(target, d)) for s, d in SINGLE_FILES]
    for name in extras:
        src, dst = OPTIONAL[name]
        pairs += walk_pairs(os.path.join(KIT, src), os.path.join(target, dst))
    for folder in FOLDERS:
        src_root = os.path.join(KIT, folder)
        for dirpath, _dirs, files in os.walk(src_root):
            for name in files:
                src = os.path.join(dirpath, name)
                rel = os.path.relpath(src, KIT)
                pairs.append((src, os.path.join(target, rel)))
    return sorted(pairs)


def install(target, dry_run=False, extras=()):
    """Copy kit files into target. Return (copied, skipped) lists of relative paths."""
    copied, skipped = [], []
    for src, dst in plan(target, extras):
        rel = os.path.relpath(dst, target)
        if os.path.exists(dst):
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
    parser = argparse.ArgumentParser(description="Copy the Addictive kit into a project.")
    parser.add_argument("target", help="your project folder")
    parser.add_argument("--dry-run", action="store_true", help="show what would be copied; change nothing")
    parser.add_argument("--with-code-graph", action="store_true",
                        help="also install the optional code-graph skill (for large projects; "
                             "needs the graphify CLI: uv tool install graphifyy)")
    args = parser.parse_args(argv)

    target = os.path.abspath(args.target)
    if not os.path.isdir(target):
        print(f"Not a folder: {target}")
        return 1
    if os.path.samefile(target, KIT):
        print("That is the kit itself. Pick your own project folder.")
        return 1

    extras = ["code-graph"] if args.with_code_graph else []
    copied, skipped = install(target, args.dry_run, extras)
    verb = "Would copy" if args.dry_run else "Copied"
    print(f"{verb} {len(copied)} files into {target}")
    for rel in copied:
        print(f"  + {rel}")
    if skipped:
        print(f"Skipped {len(skipped)} files you already have (merge by hand if you want them):")
        for rel in skipped:
            print(f"  = {rel}")
    if not args.dry_run:
        print("\nNext steps:")
        if "CLAUDE.md" in skipped:
            print(f"  1. You already have a CLAUDE.md. Copy the parts you want from {os.path.join(KIT, 'CLAUDE.md.template')}")
        else:
            print("  1. Edit CLAUDE.md: fill in the 'Project' and 'Run tests' lines.")
        print("  2. Run: python scripts/make_codemap.py")
        print("  3. No Fable access? In .claude/agents/big-decision.md change 'model: fable' to 'model: opus'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

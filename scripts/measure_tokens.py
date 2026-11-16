"""Count the tokens Claude Code really used, from its own session logs.

Claude Code saves every session as a .jsonl file under ~/.claude/projects/.
Each reply from the model records how many tokens it used. This script adds
them up, per model, and includes subagent logs, which live in a
`<session-id>/subagents/` folder next to the main log. Leaving subagents out
would make delegation look cheaper than it is.

Usage:
    python scripts/measure_tokens.py                 # latest session of this folder
    python scripts/measure_tokens.py --last 3        # last 3 sessions of this folder
    python scripts/measure_tokens.py --session ID    # one session by id
    python scripts/measure_tokens.py --project PATH  # sessions of another folder
    python scripts/measure_tokens.py --json          # machine-readable output

It only reads files on your computer. Nothing is sent anywhere.
"""

import argparse
import json
import os
import re
import sys

FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def long_path(path):
    """Windows refuses paths over 260 characters unless they start with \\\\?\\.

    Claude Code's log paths are often longer than that, so we add the prefix.
    """
    path = os.path.abspath(path)
    if os.name == "nt" and not path.startswith("\\\\?\\"):
        return "\\\\?\\" + path
    return path


def projects_dir():
    return os.path.join(os.path.expanduser("~"), ".claude", "projects")


def project_folder_name(project_path):
    """Claude Code names each project's log folder after its path, with every
    character that is not a letter, digit or dash replaced by a dash.
    Example: C:\\Users\\me\\app  ->  C--Users-me-app"""
    return re.sub(r"[^A-Za-z0-9-]", "-", os.path.abspath(project_path))


def jsonl_in(folder):
    """List the .jsonl files in a folder. We use os.listdir with the long-path
    prefix because glob silently finds nothing on very long Windows paths."""
    try:
        names = os.listdir(long_path(folder))
    except OSError:
        return []
    return sorted(os.path.join(folder, n) for n in names if n.endswith(".jsonl"))


def find_sessions(project_path):
    """Return this project's main session logs, newest first."""
    folder = os.path.join(projects_dir(), project_folder_name(project_path))
    logs = jsonl_in(folder)
    return sorted(logs, key=lambda p: os.path.getmtime(long_path(p)), reverse=True)


def subagent_logs(session_log):
    """Subagent logs for one session: <folder>/<session-id>/subagents/*.jsonl"""
    session_dir = session_log[: -len(".jsonl")]
    return jsonl_in(os.path.join(session_dir, "subagents"))


def count_file(path, totals, seen):
    """Add the token usage in one .jsonl log to `totals` (a dict keyed by model).

    The same model reply can be written on several lines (one per content
    block), each repeating the same usage numbers. We count each reply once,
    using its message id (plus request id) as the key in `seen`.
    """
    with open(long_path(path), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue  # a half-written last line while a session is running
            msg = entry.get("message")
            if not isinstance(msg, dict) or not isinstance(msg.get("usage"), dict):
                continue
            key = (msg.get("id"), entry.get("requestId"))
            if key != (None, None):
                if key in seen:
                    continue
                seen.add(key)
            model = msg.get("model") or "unknown"
            if model == "<synthetic>":
                continue  # placeholder entries written by Claude Code, not real API calls
            bucket = totals.setdefault(model, dict.fromkeys(FIELDS, 0) | {"replies": 0})
            for field in FIELDS:
                value = msg["usage"].get(field) or 0
                if isinstance(value, int):
                    bucket[field] += value
            bucket["replies"] += 1


def measure(session_log):
    """Return {"main": {...}, "subagents": {...}} token totals for one session."""
    seen = set()
    main, subs = {}, {}
    count_file(session_log, main, seen)
    for sub in subagent_logs(session_log):
        count_file(sub, subs, seen)
    return {"session": os.path.basename(session_log)[:-6], "main": main, "subagents": subs,
            "subagent_logs": len(subagent_logs(session_log))}


def add_up(per_model):
    total = dict.fromkeys(FIELDS, 0) | {"replies": 0}
    for bucket in per_model.values():
        for k in total:
            total[k] += bucket.get(k, 0)
    return total


def print_report(result):
    print(f"Session {result['session']}  (subagent logs: {result['subagent_logs']})")
    header = f"  {'part':<10} {'model':<22} {'replies':>7} {'input':>9} {'cache write':>12} {'cache read':>12} {'output':>9}"
    print(header)
    for part in ("main", "subagents"):
        for model, b in sorted(result[part].items()):
            print(f"  {part:<10} {model:<22} {b['replies']:>7} {b['input_tokens']:>9,} "
                  f"{b['cache_creation_input_tokens']:>12,} {b['cache_read_input_tokens']:>12,} {b['output_tokens']:>9,}")
    t = add_up(result["main"] | {f"sub:{k}": v for k, v in result["subagents"].items()})
    print(f"  {'TOTAL':<10} {'':<22} {t['replies']:>7} {t['input_tokens']:>9,} "
          f"{t['cache_creation_input_tokens']:>12,} {t['cache_read_input_tokens']:>12,} {t['output_tokens']:>9,}")
    print("  Note: cache reads are much cheaper than fresh input; compare like with like.")
    print()


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Sum Claude Code token usage from local session logs.")
    parser.add_argument("--project", default=".", help="project folder whose sessions to read (default: .)")
    parser.add_argument("--session", help="session id (file name without .jsonl)")
    parser.add_argument("--last", type=int, default=1, help="how many recent sessions (default: 1)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = parser.parse_args(argv)

    sessions = find_sessions(args.project)
    if args.session:
        sessions = [s for s in sessions if os.path.basename(s) == args.session + ".jsonl"]
    else:
        sessions = sessions[: max(args.last, 1)]
    if not sessions:
        print(f"No Claude Code sessions found for {os.path.abspath(args.project)}")
        print(f"(looked in {os.path.join(projects_dir(), project_folder_name(args.project))})")
        return 1

    results = [measure(s) for s in sessions]
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print_report(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())

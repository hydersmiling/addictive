"""Benchmark: does the kit save tokens without making results worse?

For every task in tasks.json it makes two fresh copies of sample_repo:
  * baseline - the plain project, no kit
  * kit      - the same project with the kit installed and CODEMAP.md built
Then it runs Claude Code headless (`claude -p`) on each copy with the same
prompt and model, and records:
  * tokens per model, read from Claude Code's own logs (subagents included)
  * cost in dollars as reported by Claude Code
  * pass/fail from hidden checks Claude never sees
  * lines added/removed in the project (smaller is better if it still passes)

IMPORTANT: a real run uses your Claude plan or API credit. Without --run the
script only prints what it would do.

Usage:
    python benchmarks/run_benchmark.py                       # dry run: show the plan
    python benchmarks/run_benchmark.py --run                 # all tasks, both modes, once
    python benchmarks/run_benchmark.py --run --repeat 3      # 3 runs each (better)
    python benchmarks/run_benchmark.py --run --tasks fix-bug --model sonnet

Results are appended to benchmarks/results/results.jsonl and summarised on screen.
"""

import argparse
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(KIT, "scripts"))
import install  # noqa: E402
import measure_tokens  # noqa: E402

SAMPLE = os.path.join(HERE, "sample_repo")
HIDDEN = os.path.join(HERE, "hidden_checks")
RESULTS = os.path.join(HERE, "results", "results.jsonl")


def sh(cmd, cwd, timeout=120):
    """Run a command; return (exit code, combined output). Never raises."""
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout,
                           shell=isinstance(cmd, str))
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)


def git_commit_all(cwd, message):
    sh(["git", "add", "-A"], cwd)
    sh(["git", "-c", "user.name=bench", "-c", "user.email=bench@example.invalid",
        "commit", "-q", "--no-verify", "-m", message], cwd)


def prepare(mode, workdir):
    """Copy the sample into workdir and, for kit mode, install the kit."""
    shutil.copytree(SAMPLE, workdir)
    sh(["git", "init", "-q"], workdir)
    if mode == "kit":
        install.install(workdir)
        claude_md = os.path.join(workdir, "CLAUDE.md")
        with open(claude_md, encoding="utf-8") as fh:
            text = fh.read()
        text = text.replace("<one line: what this project is>", "A tiny shop library (benchmark sample).")
        text = text.replace("<command, e.g. `python -m unittest` or `npm test`>",
                            "`python -m unittest discover tests`")
        with open(claude_md, "w", encoding="utf-8") as fh:
            fh.write(text)
        sh([sys.executable, os.path.join("scripts", "make_codemap.py")], workdir)
    git_commit_all(workdir, "start")  # so the diff later shows only Claude's changes


def claude_command(claude_cmd, prompt, model):
    """The headless Claude Code call. Same flags for both modes, so the test is fair.

    --setting-sources project,local : ignore your personal user settings and plugins
    --strict-mcp-config             : no MCP servers in either mode
    --permission-mode acceptEdits   : allow file edits inside the throwaway copy
    --allowedTools "Bash(python *)" : allow running Python (tests), nothing else in the shell
    """
    exe = shutil.which(claude_cmd[0]) or claude_cmd[0]
    return [exe, *claude_cmd[1:], "-p", prompt, "--output-format", "json", "--model", model,
            "--setting-sources", "project,local", "--strict-mcp-config",
            "--permission-mode", "acceptEdits", "--allowedTools", "Bash(python *)"]


def lines_changed(workdir):
    """Lines added and removed by Claude, ignoring the generated code map."""
    sh(["git", "add", "-A"], workdir)  # include new files in the count
    _code, out = sh(["git", "diff", "--cached", "--numstat", "--", ".", ":!CODEMAP.md"], workdir)
    added = removed = 0
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
            added += int(parts[0])
            removed += int(parts[1])
    return added, removed


def tokens_from_logs(workdir, session_id):
    """Token totals from Claude Code's logs for this run, subagents included."""
    folder = os.path.join(measure_tokens.projects_dir(), measure_tokens.project_folder_name(workdir))
    log = os.path.join(folder, f"{session_id}.jsonl")
    if not session_id or not os.path.exists(measure_tokens.long_path(log)):
        return None
    result = measure_tokens.measure(log)
    both = {"main:" + k: v for k, v in result["main"].items()}
    both.update({"sub:" + k: v for k, v in result["subagents"].items()})
    return {"by_model": both, "total": measure_tokens.add_up(both)}


def run_one(task, mode, model, claude_cmd, keep=False):
    """Run one task in one mode. Returns a result dict."""
    base = tempfile.mkdtemp(prefix=f"bench-{task['id']}-{mode}-")
    workdir = os.path.realpath(os.path.join(base, "repo"))
    try:
        prepare(mode, workdir)
        started = time.time()
        code, out = sh(claude_command(claude_cmd, task["prompt"], model), workdir, timeout=900)
        seconds = round(time.time() - started, 1)
        try:
            reply = json.loads(out[out.index("{"):]) if "{" in out else {}
        except json.JSONDecodeError:
            reply = {}
        answer = str(reply.get("result", ""))

        for name in task.get("hidden_files", []):
            shutil.copy2(os.path.join(HIDDEN, name), os.path.join(workdir, name))
        failures = []
        for check in task.get("checks", []):
            c_code, c_out = sh(check, workdir)
            if c_code != 0:
                failures.append(f"{check}: {c_out.strip().splitlines()[-1] if c_out.strip() else 'failed'}")
        for needle in task.get("answer_must_contain", []):
            if needle not in answer:
                failures.append(f"answer is missing '{needle}'")
        for name in task.get("hidden_files", []):
            os.remove(os.path.join(workdir, name))
        added, removed = lines_changed(workdir)

        return {
            "task": task["id"], "mode": mode, "model": model, "time": time.strftime("%Y-%m-%d %H:%M"),
            "claude_exit": code, "passed": code == 0 and not failures, "failures": failures,
            "cost_usd": reply.get("total_cost_usd"), "turns": reply.get("num_turns"),
            "seconds": seconds, "lines_added": added, "lines_removed": removed,
            "tokens": tokens_from_logs(workdir, reply.get("session_id")),
        }
    finally:
        if not keep:
            shutil.rmtree(base, ignore_errors=True)


def total_tokens(row):
    """Fresh input + cache writes + output. Cache reads are listed separately (much cheaper)."""
    t = (row.get("tokens") or {}).get("total")
    if not t:
        return None
    return t["input_tokens"] + t["cache_creation_input_tokens"] + t["output_tokens"]


def span(values):
    """'median (min-max)' for a list of numbers, or '-' if empty."""
    values = [v for v in values if v is not None]
    if not values:
        return "-"
    med = statistics.median(values)
    fmt = (lambda v: f"{v:.3f}") if isinstance(values[0], float) else (lambda v: f"{v:,}")
    return fmt(med) if len(values) == 1 else f"{fmt(med)} ({fmt(min(values))}-{fmt(max(values))})"


def summarise(rows):
    print(f"\n{'task':<12} {'mode':<9} {'pass':>6} {'tokens*':>24} {'cache read':>24} {'cost $':>20} {'lines +/-':>12}")
    for task in sorted({r["task"] for r in rows}):
        for mode in ("baseline", "kit"):
            rs = [r for r in rows if r["task"] == task and r["mode"] == mode]
            if not rs:
                continue
            passed = sum(r["passed"] for r in rs)
            cache = [((r.get("tokens") or {}).get("total") or {}).get("cache_read_input_tokens") for r in rs]
            lines = span([r["lines_added"] + r["lines_removed"] for r in rs])
            print(f"{task:<12} {mode:<9} {passed:>3}/{len(rs):<2} {span([total_tokens(r) for r in rs]):>24} "
                  f"{span(cache):>24} {span([r['cost_usd'] for r in rs]):>20} {lines:>12}")
    print("\n* tokens = fresh input + cache writes + output, all models, subagents included.")
    print("  Numbers are median (min-max). A saving only counts if the pass rate is not lower.")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Compare Claude Code with and without the kit.")
    parser.add_argument("--run", action="store_true", help="really run Claude (uses your plan/credit)")
    parser.add_argument("--tasks", nargs="*", help="task ids to run (default: all)")
    parser.add_argument("--modes", nargs="*", default=["baseline", "kit"], choices=["baseline", "kit"])
    parser.add_argument("--repeat", type=int, default=1, help="runs per task and mode (3+ recommended)")
    parser.add_argument("--model", default="opus", help="main model for both modes (default: opus)")
    parser.add_argument("--claude-cmd", default="claude", help="command that starts Claude Code")
    parser.add_argument("--keep", action="store_true", help="keep the temporary project copies")
    parser.add_argument("--out", default=RESULTS, help="where to append results (JSON lines)")
    args = parser.parse_args(argv)

    with open(os.path.join(HERE, "tasks.json"), encoding="utf-8") as fh:
        tasks = json.load(fh)["tasks"]
    if args.tasks:
        tasks = [t for t in tasks if t["id"] in args.tasks]
    runs = [(t, m) for t in tasks for m in args.modes for _ in range(args.repeat)]

    print(f"{len(runs)} runs: {len(tasks)} tasks x {len(args.modes)} modes x {args.repeat} repeats, model {args.model}")
    if not args.run:
        for t, m in runs:
            print(f"  would run  {t['id']:<12} {m}")
        print("\nDry run only. Add --run to really run Claude (this uses your plan or API credit).")
        return 0

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    rows = []
    claude_cmd = args.claude_cmd.split()
    for i, (task, mode) in enumerate(runs, 1):
        print(f"[{i}/{len(runs)}] {task['id']} {mode} ...", flush=True)
        row = run_one(task, mode, args.model, claude_cmd, args.keep)
        rows.append(row)
        with open(args.out, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
        status = "pass" if row["passed"] else "FAIL " + "; ".join(row["failures"])[:120]
        print(f"    {status} | tokens {total_tokens(row)} | cost {row['cost_usd']} | lines +{row['lines_added']}/-{row['lines_removed']}")
    summarise(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())

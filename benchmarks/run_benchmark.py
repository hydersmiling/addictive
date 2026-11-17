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

sys.path.insert(0, HERE)
import build_audit_sample  # noqa: E402

SAMPLE = os.path.join(HERE, "sample_repo")
HIDDEN = os.path.join(HERE, "hidden_checks")
# name -> (project folder, task file, folder of hidden checks)
SAMPLES = {
    "small": (SAMPLE, os.path.join(HERE, "tasks.json"), HIDDEN),
    "large": (os.path.join(HERE, "sample_large"), os.path.join(HERE, "tasks_large.json"),
              os.path.join(HERE, "hidden_checks_large")),
    # Built on the fly (large sample + 150 legacy modules) instead of stored in git.
    "audit": (build_audit_sample.build, os.path.join(HERE, "tasks_audit.json"), HIDDEN),
    # All six large+audit tasks in ONE session on the audit sample (see run_session).
    "session": (build_audit_sample.build, os.path.join(HERE, "tasks_session.json"),
                os.path.join(HERE, "hidden_checks_large")),
}
RESULTS = os.path.join(HERE, "results", "results.jsonl")


def sh(cmd, cwd, timeout=120, stdout_only=False):
    """Run a command; return (exit code, output). Never raises.

    Output is stdout+stderr, or stdout alone with stdout_only=True (for JSON replies)."""
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout,
                           shell=isinstance(cmd, str))
        return p.returncode, (p.stdout or "") + ("" if stdout_only else (p.stderr or ""))
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)


def git_commit_all(cwd, message):
    sh(["git", "add", "-A"], cwd)
    sh(["git", "-c", "user.name=bench", "-c", "user.email=bench@example.invalid",
        "commit", "-q", "--no-verify", "-m", message], cwd)


def load_tasks(sample):
    """(project line, task list) for a sample."""
    with open(SAMPLES[sample][1], encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("project_line", "A tiny shop library (benchmark sample)."), data["tasks"]


def prepare(mode, workdir, sample="small"):
    """Copy the sample into workdir and, for kit mode, install the kit."""
    source = SAMPLES[sample][0]
    if callable(source):
        source(workdir)  # a builder function creates the sample
    else:
        shutil.copytree(source, workdir)
    sh(["git", "init", "-q"], workdir)
    if mode == "kit":
        install.install(workdir)
        claude_md = os.path.join(workdir, "CLAUDE.md")
        with open(claude_md, encoding="utf-8") as fh:
            text = fh.read()
        text = text.replace("<one line: what this project is>", load_tasks(sample)[0])
        text = text.replace("<command, e.g. `python -m unittest` or `npm test`>",
                            "`python -m unittest discover tests`")
        with open(claude_md, "w", encoding="utf-8") as fh:
            fh.write(text)
        sh([sys.executable, os.path.join("scripts", "make_codemap.py")], workdir)
    git_commit_all(workdir, "start")  # so the diff later shows only Claude's changes


def claude_command(claude_cmd, prompt, model, effort=None):
    """The headless Claude Code call. Same flags for both modes, so the test is fair.

    --setting-sources project,local : ignore your personal user settings and plugins
    --strict-mcp-config             : no MCP servers in either mode
    --permission-mode acceptEdits   : allow file edits inside the throwaway copy
    --allowedTools "Bash(python *)" : allow running Python (tests), nothing else in the shell
    """
    exe = shutil.which(claude_cmd[0]) or claude_cmd[0]
    cmd = [exe, *claude_cmd[1:], "-p", prompt, "--output-format", "json", "--model", model,
           "--setting-sources", "project,local", "--strict-mcp-config",
           "--permission-mode", "acceptEdits", "--allowedTools", "Bash(python *)"]
    if effort:
        cmd += ["--effort", effort]
    return cmd


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


def code_diff(workdir, limit=20000):
    """The code Claude changed, as a unified diff (kept for the blind quality review)."""
    _code, out = sh(["git", "diff", "--cached", "--", ".", ":!CODEMAP.md"], workdir)
    return out[:limit]


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


def run_one(task, mode, model, claude_cmd, keep=False, sample="small", effort=None):
    """Run one task in one mode. Returns a result dict."""
    base = tempfile.mkdtemp(prefix=f"bench-{task['id']}-{mode}-")
    workdir = os.path.realpath(os.path.join(base, "repo"))
    try:
        prepare(mode, workdir, sample)
        started = time.time()
        code, out = sh(claude_command(claude_cmd, task["prompt"], model, effort), workdir, timeout=900, stdout_only=True)
        seconds = round(time.time() - started, 1)
        try:
            reply = json.JSONDecoder().raw_decode(out[out.index("{"):])[0] if "{" in out else {}
        except json.JSONDecodeError:
            reply = {}
        if not reply:
            print("    warning: could not read Claude's JSON reply; cost and tokens will be missing")
        answer = str(reply.get("result", ""))

        failures = []
        copied = []
        for name in task.get("hidden_files", []):
            dst = os.path.join(workdir, name)
            if os.path.lexists(dst):  # never overwrite a file Claude created or changed
                failures.append(f"hidden file {name} clashes with a project file")
                continue
            shutil.copy2(os.path.join(SAMPLES[sample][2], name), dst)
            copied.append(name)
        for check in task.get("checks", []):
            c_code, c_out = sh(check, workdir)
            if c_code != 0:
                failures.append(f"{check}: {c_out.strip().splitlines()[-1] if c_out.strip() else 'failed'}")
        for needle in task.get("answer_must_contain", []):
            if needle not in answer:
                failures.append(f"answer is missing '{needle}'")
        for needle in task.get("answer_must_not_contain", []):
            if needle in answer:
                failures.append(f"answer wrongly includes '{needle}'")
        for name in copied:
            os.remove(os.path.join(workdir, name))
        added, removed = lines_changed(workdir)
        diff = code_diff(workdir)

        return {
            "task": task["id"], "mode": mode, "model": model, "sample": sample, "time": time.strftime("%Y-%m-%d %H:%M"),
            "claude_exit": code, "passed": code == 0 and not failures, "failures": failures,
            "cost_usd": reply.get("total_cost_usd"), "turns": reply.get("num_turns"),
            "seconds": seconds, "lines_added": added, "lines_removed": removed,
            "tokens": tokens_from_logs(workdir, reply.get("session_id")),
            "diff": diff, "answer": answer[:4000],
        }
    finally:
        if not keep:
            shutil.rmtree(base, ignore_errors=True)


def tokens_from_sessions(workdir, session_ids):
    """Token totals across every log a resumed session wrote, each reply counted once."""
    folder = os.path.join(measure_tokens.projects_dir(), measure_tokens.project_folder_name(workdir))
    seen, main, subs = set(), {}, {}
    found = False
    for sid in dict.fromkeys(s for s in session_ids if s):  # unique, in order
        log = os.path.join(folder, f"{sid}.jsonl")
        if not os.path.exists(measure_tokens.long_path(log)):
            continue
        found = True
        measure_tokens.count_file(log, main, seen)
        for sub in measure_tokens.subagent_logs(log):
            measure_tokens.count_file(sub, subs, seen)
    if not found:
        return None
    both = {"main:" + k: v for k, v in main.items()}
    both.update({"sub:" + k: v for k, v in subs.items()})
    return {"by_model": both, "total": measure_tokens.add_up(both)}


def run_session(tasks, mode, model, claude_cmd, keep=False, sample="session", effort=None):
    """Run every task, one after another, in ONE Claude Code session (resumed between tasks).

    This is how people actually work: the conversation grows with each task, so every
    later reply re-reads more context. Checks run once at the end; answer checks apply
    to each task's own reply. Returns one result dict for the whole session."""
    base = tempfile.mkdtemp(prefix=f"bench-session-{mode}-")
    workdir = os.path.realpath(os.path.join(base, "repo"))
    try:
        prepare(mode, workdir, sample)
        started = time.time()
        session_ids, answers, cost, turns, exit_codes = [], {}, 0.0, 0, []
        sid = None
        for task in tasks:
            cmd = claude_command(claude_cmd, task["prompt"], model, effort)
            if sid:
                cmd += ["--resume", sid]  # continue the same conversation
            code, out = sh(cmd, workdir, timeout=900, stdout_only=True)
            exit_codes.append(code)
            try:
                reply = json.JSONDecoder().raw_decode(out[out.index("{"):])[0] if "{" in out else {}
            except json.JSONDecodeError:
                reply = {}
            sid = reply.get("session_id") or sid
            session_ids.append(reply.get("session_id"))
            answers[task["id"]] = str(reply.get("result", ""))
            cost += reply.get("total_cost_usd") or 0
            turns += reply.get("num_turns") or 0
        seconds = round(time.time() - started, 1)

        task_results = {}
        hidden = {n for t in tasks for n in t.get("hidden_files", [])}
        copied = []
        for name in sorted(hidden):
            dst = os.path.join(workdir, name)
            if not os.path.lexists(dst):
                shutil.copy2(os.path.join(SAMPLES[sample][2], name), dst)
                copied.append(name)
        for task in tasks:
            failures = []
            for check in task.get("checks", []):
                c_code, c_out = sh(check, workdir)
                if c_code != 0:
                    failures.append(f"{check}: {c_out.strip().splitlines()[-1] if c_out.strip() else 'failed'}")
            answer = answers.get(task["id"], "")
            failures += [f"answer is missing '{n}'" for n in task.get("answer_must_contain", []) if n not in answer]
            failures += [f"answer wrongly includes '{n}'" for n in task.get("answer_must_not_contain", []) if n in answer]
            task_results[task["id"]] = failures
        for name in copied:
            os.remove(os.path.join(workdir, name))
        added, removed = lines_changed(workdir)

        failures = [f"{t}: {f}" for t, fs in task_results.items() for f in fs]
        return {
            "task": f"session({len(tasks)})", "mode": mode, "model": model, "sample": sample,
            "time": time.strftime("%Y-%m-%d %H:%M"), "claude_exit": max(exit_codes or [1]),
            "passed": not failures and not any(exit_codes), "failures": failures,
            "tasks_passed": sum(not fs for fs in task_results.values()), "tasks_total": len(tasks),
            "cost_usd": round(cost, 6), "turns": turns, "seconds": seconds,
            "lines_added": added, "lines_removed": removed,
            "tokens": tokens_from_sessions(workdir, session_ids), "diff": code_diff(workdir),
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
    parser.add_argument("--model", default="opus", help="main model (default: opus)")
    parser.add_argument("--kit-model", help="main model for kit runs only (default: same as --model)")
    parser.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"],
                        help="effort level for every run (default: Claude Code's own)")
    parser.add_argument("--claude-cmd", default="claude", help="command that starts Claude Code")
    parser.add_argument("--keep", action="store_true", help="keep the temporary project copies")
    parser.add_argument("--sample", default="small", choices=sorted(SAMPLES), help="which sample project")
    parser.add_argument("--max-tokens", type=int, default=0,
                        help="stop starting new runs once this many tokens* are used (0 = no limit)")
    parser.add_argument("--out", default=RESULTS, help="where to append results (JSON lines)")
    args = parser.parse_args(argv)

    tasks = load_tasks(args.sample)[1]
    if args.tasks:
        tasks = [t for t in tasks if t["id"] in args.tasks]
    # Round by round (all tasks, both modes), so a budget stop keeps the comparison balanced.
    # The session sample runs all its tasks as one unit per mode.
    units = [{"id": f"session({len(tasks)})", "tasks": tasks}] if args.sample == "session" else tasks
    runs = [(t, m) for _ in range(args.repeat) for t in units for m in args.modes]

    print(f"{len(runs)} runs on the {args.sample} sample: {len(tasks)} tasks x {len(args.modes)} modes "
          f"x {args.repeat} repeats, model {args.model}")
    if not args.run:
        for t, m in runs:
            print(f"  would run  {t['id']:<12} {m}")
        print("\nDry run only. Add --run to really run Claude (this uses your plan or API credit).")
        return 0

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    rows = []
    claude_cmd = [args.claude_cmd]  # one path; may contain spaces on Windows
    used = 0
    for i, (task, mode) in enumerate(runs, 1):
        if args.max_tokens and used >= args.max_tokens:
            print(f"Token budget reached ({used:,} of {args.max_tokens:,}); skipping the remaining runs.")
            break
        print(f"[{i}/{len(runs)}] {task['id']} {mode} ...", flush=True)
        model = args.kit_model if (mode == "kit" and args.kit_model) else args.model
        if args.sample == "session":
            row = run_session(task["tasks"], mode, model, claude_cmd, args.keep, args.sample, args.effort)
        else:
            row = run_one(task, mode, model, claude_cmd, args.keep, args.sample, args.effort)
        rows.append(row)
        with open(args.out, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
        tokens = total_tokens(row)
        status = "pass" if row["passed"] else "FAIL " + "; ".join(row["failures"])[:120]
        print(f"    {status} | tokens {tokens} | cost {row['cost_usd']} | lines +{row['lines_added']}/-{row['lines_removed']}")
        if args.max_tokens and tokens is None:
            print("Token log unreadable for that run, so the budget can't be enforced; stopping.")
            break  # fail closed: an unknown spend must not let the budget run open
        used += tokens
    summarise(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())

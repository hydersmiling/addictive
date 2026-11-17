"""Blind quality review: does the kit's output look as good as plain Claude's?

The benchmark's hidden tests check that code *works*. This script checks how it
*reads*. For every task, it pairs a baseline run with a kit run, hides which is
which (the order is shuffled and labelled A/B), and asks a reviewer model to
score both on correctness, readability, minimal scope and fit with the codebase.

Usage:
    python benchmarks/judge.py RESULTS.jsonl                 # dry run: show the pairs
    python benchmarks/judge.py RESULTS.jsonl --run           # judge them (uses your plan/credit)
    python benchmarks/judge.py RESULTS.jsonl --run --model opus

Only runs that recorded a diff or answer can be judged (benchmark runs from
version 1.1 on). Judgements are appended to benchmarks/results/judgements.jsonl.
"""

import argparse
import json
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results", "judgements.jsonl")
CRITERIA = ["correctness", "readability", "minimal_scope", "fits_codebase"]

PROMPT = """You are reviewing two solutions to the same coding task. You do not know who wrote them.
Task: {task}

Solution A:
{a}

Solution B:
{b}

Score each solution from 1 to 10 on: correctness, readability, minimal_scope (changes only
what the task needs), fits_codebase (reuses existing helpers and matches local style).
Reply with JSON only, no prose:
{{"A": {{"correctness": n, "readability": n, "minimal_scope": n, "fits_codebase": n}},
  "B": {{"correctness": n, "readability": n, "minimal_scope": n, "fits_codebase": n}},
  "better": "A" | "B" | "tie", "reason": "<one sentence>"}}"""


def solution_text(row):
    """What the reviewer sees: the code diff, or the text answer for read-only tasks."""
    return row.get("diff") or row.get("answer") or "(no change)"


def make_pairs(rows):
    """Pair baseline and kit runs of the same sample and task, in order of appearance."""
    pairs, waiting = [], {}
    for row in rows:
        if not (row.get("diff") or row.get("answer")):
            continue  # older runs did not record their output
        key = (row.get("sample", "small"), row["task"])
        slot = waiting.setdefault(key, {"baseline": [], "kit": []})
        slot[row["mode"]].append(row)
        if slot["baseline"] and slot["kit"]:
            pairs.append((slot["baseline"].pop(0), slot["kit"].pop(0)))
    return pairs


def judge_pair(base, kit, prompt_text, claude_cmd, model, rng):
    """Ask the reviewer to score one blind pair. Returns a judgement dict."""
    kit_is_a = rng.random() < 0.5
    a, b = (kit, base) if kit_is_a else (base, kit)
    text = PROMPT.format(task=prompt_text, a=solution_text(a), b=solution_text(b))
    exe = shutil.which(claude_cmd[0]) or claude_cmd[0]
    cmd = [exe, *claude_cmd[1:], "-p", text, "--output-format", "json", "--model", model,
           "--setting-sources", "project,local", "--strict-mcp-config", "--tools", ""]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        reply = json.JSONDecoder().raw_decode(proc.stdout[proc.stdout.index("{"):])[0]
        result = reply.get("result", reply)
        verdict = json.loads(result[result.index("{"):result.rindex("}") + 1]) if isinstance(result, str) else result
    except (ValueError, json.JSONDecodeError):
        return {"task": base["task"], "error": "could not read the reviewer's reply"}
    kit_label, base_label = ("A", "B") if kit_is_a else ("B", "A")
    better = verdict.get("better")
    return {
        "task": base["task"], "sample": base.get("sample", "small"),
        "models": {"baseline": base["model"], "kit": kit["model"]},
        "kit": verdict.get(kit_label), "baseline": verdict.get(base_label),
        "winner": "kit" if better == kit_label else "baseline" if better == base_label else "tie",
        "reason": verdict.get("reason", ""), "reviewer": model,
    }


def summarise(judgements):
    ok = [j for j in judgements if "error" not in j]
    if not ok:
        print("No judgements to summarise.")
        return
    wins = {w: sum(j["winner"] == w for j in ok) for w in ("kit", "baseline", "tie")}
    print(f"\n{len(ok)} blind comparisons: kit better {wins['kit']}, baseline better "
          f"{wins['baseline']}, tie {wins['tie']}")
    for crit in CRITERIA:
        k = sum((j["kit"] or {}).get(crit, 0) for j in ok) / len(ok)
        b = sum((j["baseline"] or {}).get(crit, 0) for j in ok) / len(ok)
        print(f"  {crit:<14} kit {k:4.1f}   baseline {b:4.1f}")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Blind A/B quality review of benchmark outputs.")
    parser.add_argument("results", help="a results .jsonl file from run_benchmark.py")
    parser.add_argument("--run", action="store_true", help="really call the reviewer (uses your plan/credit)")
    parser.add_argument("--model", default="opus", help="reviewer model (default: opus)")
    parser.add_argument("--claude-cmd", default="claude")
    parser.add_argument("--seed", type=int, default=1, help="shuffle seed for the A/B order")
    parser.add_argument("--out", default=OUT)
    args = parser.parse_args(argv)

    with open(args.results, encoding="utf-8") as fh:
        rows = [json.loads(line) for line in fh if line.strip()]
    pairs = make_pairs(rows)
    print(f"{len(pairs)} baseline/kit pairs can be judged.")
    if not args.run:
        for base, kit in pairs:
            print(f"  would judge {base['task']:<12} {base['model']} plain vs {kit['model']} + kit")
        print("\nDry run only. Add --run to call the reviewer.")
        return 0

    prompts = {}
    for name in ("tasks.json", "tasks_large.json", "tasks_audit.json"):
        with open(os.path.join(HERE, name), encoding="utf-8") as fh:
            for t in json.load(fh)["tasks"]:
                prompts.setdefault(t["id"], t["prompt"])
    rng = random.Random(args.seed)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    judgements = []
    for base, kit in pairs:
        j = judge_pair(base, kit, prompts.get(base["task"], base["task"]), [args.claude_cmd], args.model, rng)
        judgements.append(j)
        with open(args.out, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(j) + "\n")
        print(f"  {j['task']:<12} winner: {j.get('winner', 'error')}")
    summarise(judgements)
    return 0


if __name__ == "__main__":
    sys.exit(main())

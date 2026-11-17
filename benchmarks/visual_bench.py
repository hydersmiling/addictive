"""Visual benchmark: does Sonnet + Mainseat produce pages that look as good as plain Opus?

Each setup gets the same prompt in a fresh, empty folder. The finished page is
screenshotted, and an Opus judge scores all screenshots blind: they are shown as
A, B, C in a random order, without saying which setup made which.

Usage:
    python benchmarks/visual_bench.py                     # dry run: show the plan
    python benchmarks/visual_bench.py --run --rounds 2    # really run (uses your plan/credit)

Results go to benchmarks/results/visual/ (ignored by git, so nothing is published).
Run it from a normal terminal: some sandboxes block the headless browser used for screenshots.
"""

import argparse
import glob
import json
import os
import random
import shutil
import string
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(KIT, "scripts"))
import install  # noqa: E402
import screenshot  # noqa: E402

OUT = os.path.join(HERE, "results", "visual")
PROMPT = ("Build a single-page website advertising Seatly, a premium ergonomic office chair brand. "
          "Put everything in index.html (CSS inline). Make it look professional and ready to show customers.")
# name -> (main model, whether Mainseat is installed)
SETUPS = {"opus-plain": ("opus", False), "sonnet-plain": ("sonnet", False), "sonnet-mainseat": ("sonnet", True)}
CRITERIA = ["visual_quality", "polish", "brand_fit", "completeness"]

JUDGE_PROMPT = """You are judging websites built from the same brief. You do not know who built them.
Brief: {brief}

Open and look at each screenshot file:
{files}

Score each from 1 to 10 on: visual_quality (how good it looks), polish (finished, consistent,
no placeholders), brand_fit (feels like a premium brand), completeness (a customer has what
they need). Then rank them, best first.
Reply with JSON only, no prose:
{{"scores": {{"A": {{"visual_quality": n, "polish": n, "brand_fit": n, "completeness": n}}, ...}},
  "ranking": ["A", ...], "reason": "<one sentence>"}}"""


def claude_exe(claude_cmd):
    return [shutil.which(claude_cmd[0]) or claude_cmd[0], *claude_cmd[1:]]


def parse_reply(stdout):
    """Claude's --output-format json reply as a dict ({} if unreadable)."""
    try:
        return json.JSONDecoder().raw_decode(stdout[stdout.index("{"):])[0]
    except (ValueError, json.JSONDecodeError):
        return {}


def run_setup(name, prompt, claude_cmd, out_dir, keep=False):
    """Build the page with one setup; screenshot it into out_dir. Returns a result dict."""
    model, with_kit = SETUPS[name]
    base = tempfile.mkdtemp(prefix=f"visual-{name}-")
    work = os.path.join(base, "site")
    os.makedirs(work)
    try:
        if with_kit:
            install.install(work)
            path = os.path.join(work, "CLAUDE.md")
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            text = text.replace("<one line: what this project is>", "A marketing website (benchmark).")
            text = text.replace("<command, e.g. `python -m unittest` or `npm test`>", "none (static site)")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
        cmd = claude_exe(claude_cmd) + ["-p", prompt, "--output-format", "json", "--model", model,
                                        "--setting-sources", "project,local", "--strict-mcp-config",
                                        "--permission-mode", "acceptEdits", "--allowedTools", "Bash(python *)"]
        started = time.time()
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=1800)
        reply = parse_reply(proc.stdout)
        pages = sorted(glob.glob(os.path.join(work, "*.html")))
        page = os.path.join(work, "index.html") if os.path.exists(os.path.join(work, "index.html")) else (pages[0] if pages else None)
        png = None
        if page:
            os.makedirs(out_dir, exist_ok=True)
            shutil.copy2(page, os.path.join(out_dir, f"{name}.html"))
            png = screenshot.take(page, os.path.join(out_dir, f"{name}.png"))
        return {"setup": name, "model": model, "kit": with_kit, "cost_usd": reply.get("total_cost_usd"),
                "turns": reply.get("num_turns"), "seconds": round(time.time() - started),
                "page": bool(page), "screenshot": png}
    finally:
        if not keep:
            shutil.rmtree(base, ignore_errors=True)


def judge(shots, brief, claude_cmd, model="opus", rng=None):
    """Blind-score screenshots. shots: {setup: png path}. Returns {setup: scores}, ranking, reason."""
    rng = rng or random.Random()
    names = list(shots)
    rng.shuffle(names)
    letters = dict(zip(string.ascii_uppercase, names))
    files = "\n".join(f"{letter}: {os.path.abspath(shots[name])}" for letter, name in letters.items())
    cmd = claude_exe(claude_cmd) + ["-p", JUDGE_PROMPT.format(brief=brief, files=files), "--output-format", "json",
                                    "--model", model, "--setting-sources", "project,local",
                                    "--strict-mcp-config", "--allowedTools", "Read"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    reply = parse_reply(proc.stdout)
    result = reply.get("result", reply)
    try:
        verdict = json.loads(result[result.index("{"):result.rindex("}") + 1]) if isinstance(result, str) else result
    except (ValueError, json.JSONDecodeError):
        return {"error": "could not read the judge's reply"}
    return {
        "scores": {letters[k]: v for k, v in verdict.get("scores", {}).items() if k in letters},
        "ranking": [letters[k] for k in verdict.get("ranking", []) if k in letters],
        "reason": verdict.get("reason", ""), "judge_cost_usd": reply.get("total_cost_usd"),
    }


def summarise(rounds):
    print("\nsetup              avg score   avg rank   total cost")
    for name in SETUPS:
        scores, ranks, cost = [], [], 0.0
        for r in rounds:
            run = r["runs"].get(name) or {}
            cost += run.get("cost_usd") or 0
            j = r.get("judge") or {}
            if name in j.get("scores", {}):
                scores.append(sum(j["scores"][name].get(c, 0) for c in CRITERIA) / len(CRITERIA))
            if name in j.get("ranking", []):
                ranks.append(j["ranking"].index(name) + 1)
        avg = lambda xs: f"{sum(xs) / len(xs):.1f}" if xs else "-"
        print(f"{name:<18} {avg(scores):>9}   {avg(ranks):>8}   ${cost:.2f}")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Blind visual comparison of setups.")
    parser.add_argument("--run", action="store_true", help="really run (uses your plan/credit)")
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--setups", nargs="+", default=list(SETUPS), choices=list(SETUPS))
    parser.add_argument("--prompt", default=PROMPT)
    parser.add_argument("--judge-model", default="opus")
    parser.add_argument("--claude-cmd", default="claude")
    parser.add_argument("--out", default=OUT)
    args = parser.parse_args(argv)

    print(f"{args.rounds} round(s) x {len(args.setups)} setups: {', '.join(args.setups)}; judge: {args.judge_model}")
    if not args.run:
        print("Dry run only. Add --run to build the pages and judge them (uses your plan or API credit).")
        return 0
    rounds = []
    for i in range(1, args.rounds + 1):
        out_dir = os.path.join(args.out, f"round{i}")
        runs = {}
        for name in args.setups:
            print(f"[round {i}] building with {name} ...", flush=True)
            runs[name] = run_setup(name, args.prompt, [args.claude_cmd], out_dir)
            print(f"    cost {runs[name]['cost_usd']} | {runs[name]['seconds']} s | screenshot {bool(runs[name]['screenshot'])}")
        shots = {n: r["screenshot"] for n, r in runs.items() if r["screenshot"]}
        verdict = judge(shots, args.prompt, [args.claude_cmd], args.judge_model, random.Random(i)) if len(shots) > 1 else {}
        print(f"[round {i}] ranking: {verdict.get('ranking')} | {verdict.get('reason', '')[:160]}")
        rounds.append({"round": i, "runs": runs, "judge": verdict})
        os.makedirs(args.out, exist_ok=True)
        with open(os.path.join(args.out, "results.json"), "w", encoding="utf-8") as fh:
            json.dump(rounds, fh, indent=2)
    summarise(rounds)
    return 0


if __name__ == "__main__":
    sys.exit(main())

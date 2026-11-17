# Benchmark results

## Run 8: 2026-11-17, long sessions (6 tasks in one session)
All six large and audit tasks run one after another in a single resumed session on the
214-file audit sample, so context grows as in real work. One session per setup.
Costs are computed from raw token counts at list prices (Claude Code reports a running total
for resumed sessions, which an earlier version of the runner wrongly summed).

| Setup | Tasks passed | Est. cost | vs plain Opus | Main-session turns | Lines changed |
|---|---|---|---|---|---|
| Plain Opus | 6/6 | $0.53 | - | 37 | 48 |
| Sonnet + kit | 6/6 | $0.23 | -57% | 36 | 22 |
| Plain Sonnet | 6/6 | $0.15 | -71% | 20 | 39 |

Over a long session the pattern holds: Sonnet in the main seat delivers the same results for
well under half the cost; the kit adds cost over plain Sonnet (+48%) and keeps changes smallest.

## Run 7: 2026-11-17, blind quality review (plain Opus vs Sonnet + kit)
Six tasks (large + audit samples), outputs recorded, then reviewed blind by Opus: each pair
shown as A/B in random order. Benchmark cost: Opus $1.19, Sonnet + kit $0.46 (-61%); all 12
runs passed. Lines changed: 60 vs 22.

| Criterion (1-10) | Sonnet + kit | Plain Opus |
|---|---|---|
| Correctness | 8.5 | 8.8 |
| Readability | 9.0 | 9.0 |
| Minimal scope | **10.0** | 8.7 |
| Fits the codebase | 8.8 | 9.0 |
| Verdicts | 1 win | 1 win (4 ties) |

- The kit won the bug fix (same one-line fix, no unrequested files). Plain Opus won the feature
  task: it reused an existing helper so one item reads "1 item"; the kit's version said "1 items".
- A first review was discarded: the judge showed large-sample pairs the small sample's task
  text. Fixed and rerun; the invalid verdicts are kept in `judgements_invalid.jsonl` locally.
- An earlier attempt at this run exposed a real defect: when `runner` was refused permission to
  run tests, the Sonnet session stopped instead of running them itself. The template now falls
  back to the main session; the rerun passed.


## Run 6: 2026-11-17, Haiku vs Sonnet vs Opus main, small sample (1 repeat)
The 4 small-sample tasks, each main model with and without the kit. 24 runs, about $2.

| Main model | Passed (plain / kit) | Cost for 4 tasks (plain / kit) | Change | Lines changed (plain / kit) |
|---|---|---|---|---|
| Haiku | 4/4 / 4/4 | $0.024 / $0.024 | 0% | 31 / 26 |
| Sonnet | 4/4 / 4/4 | $0.263 / $0.331 | +26% | 32 / 19 |
| Opus | 4/4 / 4/4 | $0.593 / $0.794 | +34% | 39 / 27 |

### What it shows
- **Every model passed every task**, with and without the kit.
- **Model choice dwarfs everything else:** Sonnet costs ~45% of Opus, Haiku ~4%.
- **On a tiny project the kit costs more on Sonnet and Opus** (its rules are re-read every
  turn) but **always produced smaller changes** (19 vs 32 lines on Sonnet).


## Run 5: 2026-11-17, which main model? (1 repeat, large + audit samples)
Same 6 tasks, three setups: plain Opus, plain Sonnet, and Sonnet with the kit (Opus
available through the `planner` agent). Total cost about $2.

| Setup | Passed | Cost for 6 tasks | vs plain Opus | Lines changed, feature task |
|---|---|---|---|---|
| Plain Opus | 6/6 | $1.12 | - | 22 |
| Plain Sonnet | 6/6 | $0.40 | -64% | 18 |
| Sonnet + kit | 6/6 | $0.49 | -56% | 6 |

### What it shows
- **The main model is the biggest lever.** Sonnet matched Opus on every task at about a
  third of the cost.
- **The kit adds ~22% on top of plain Sonnet** on short tasks (its rules are re-read every
  turn), and its routing rarely triggered: the planner was never called, Haiku once.
- **It did keep changes smallest** (6 lines on the feature task vs 18 and 22).
- Recommendation: Sonnet as main session; Opus only through `planner` for design work.


## Run 4: 2026-11-17, Opus 5.5 main session, strict delegation, 1 repeat
The template now forbids the main session from reading, searching, editing or running
commands itself; Haiku and Sonnet helpers do all hands-on work. Large sample (4 tasks)
and audit sample (2 tasks), 12 runs, total cost $2.45.

| Task | Pass (base / kit) | Cost $ (base / kit) | Change | Opus turns (base / kit) | Kit tokens by model (Opus / Sonnet / Haiku) |
|---|---|---|---|---|---|
| fix-bug | pass / pass | 0.178 / 0.272 | +53% | 7 / 5 | 15.8k / 25.3k / 7.7k |
| add-feature | pass / pass | 0.317 / 0.271 | -14% | 15 / 2 | 19.3k / 8.9k / 29.2k |
| locate | pass / pass | 0.094 / 0.121 | +29% | 2 / 2 | 12.6k / - / 7.8k |
| rename | pass / pass | 0.199 / 0.352 | +77% | 16 / 3 | 21.8k / 16.2k / 19.6k |
| audit-money | pass / pass | 0.164 / 0.195 | +19% | 5 / 2 | 16.8k / - / 46.7k |
| audit-sql | pass / pass | 0.138 / 0.145 | +5% | 4 / 3 | 13.4k / - / 35.7k |
| **Total** | 6/6 / 6/6 | **1.09 / 1.36** | **+25%** | 49 / 17 | |

### What it shows
- **Delegation now works as designed:** every kit run used helpers, and Opus took 65% fewer
  turns (17 vs 49). Quality held: 12/12 passes.
- **But cost rose 25%.** Opus's own tokens barely fell: each Opus session has a fixed floor
  of about 12-14k tokens (system prompt and tools), and on these tasks the plain Opus run
  needs little more than that floor. The helpers' tokens are then added on top, and
  Sonnet is not cheap ($2 / $10 per million).
- **Where it cost less:** the feature task (-14%), the one where plain Opus did the most
  work itself (15 turns).
- **Hypothesis, not yet measured:** savings should grow in long sessions, where every extra
  Opus turn re-reads a growing context. These one-task runs are too short to show that.


## Run 3: 2026-11-17, Haiku 5.5, 2 repeats, audit sample (214 files)
Search-heavy tasks built to test delegation: the large sample plus 150 legacy modules
(about 630 KB), with planted problems to find and correct decoys that must not be reported.
Template updated to send audits to `explorer`. 8 runs, total cost about $0.04.

| Task | Pass (base / kit) | Tokens* (base / kit) | Change | Subagent used (kit) |
|---|---|---|---|---|
| audit-money | 2/2 / 2/2 | 13,575 / 24,495 | +80% | 1 of 2 runs |
| audit-sql | 2/2 / 2/2 | 15,438 / 15,702 | +2% | 0 of 2 runs |

### What it shows
- **Quality held:** every planted file found, no decoy reported, in both setups.
- **Delegation happened once, and cost more:** main 16.8k + `explorer` 14.8k = 31.6k tokens,
  against 13.5k for a baseline that solved the task with a few greps. When a search can be
  done with grep, handing it to a subagent duplicates work.
- **Why price can't show a saving here:** the main session was Haiku too, so the helper was no
  cheaper per token. With Opus as the main model, Haiku tokens cost 40x less, so a run can
  use more tokens and still cost less. That needs an Opus run of these tasks.


## Run 2: 2026-11-17, Opus 5.5, 2 repeats, large sample (64 files)
Method: `run_benchmark.py --run --sample large --model opus --repeat 2 --max-tokens 950000`.
Same rules as run 1. Four runs that failed with zero tokens (a usage limit was hit mid-run)
were discarded and rerun. 16 valid runs; total cost $2.93; 237,705 tokens* plus 3.6M cache
reads (cache reads cost 20x less than fresh input).

| Task | Pass (base / kit) | Tokens* (base / kit) | Change | Cost $ (base / kit) | Lines changed (base / kit) |
|---|---|---|---|---|---|
| fix-bug | 2/2 / 2/2 | 14,446 / 15,338 | +6% | 0.179 / 0.201 | 13 / 8.5 |
| add-feature | 2/2 / 2/2 | 16,917 / 16,972 | +0% | 0.209 / 0.226 | 23.5 / 7 |
| locate | 2/2 / 2/2 | 9,786 / 11,836 | +21% | 0.094 / 0.111 | 0 / 0 |
| rename | 2/2 / 2/2 | 16,667 / 16,892 | +1% | 0.231 / 0.214 | 14 / 14 |

Medians of 2 runs. Total cost: baseline about $1.43, kit about $1.50 (+5%).

### What it shows
- **Quality held:** 16/16 passes, including the hidden check that the new feature reuses
  the existing money helper.
- **Smaller changes:** the kit's diffs were 3.4x smaller on the feature task (7 vs 23.5
  lines) and a third smaller on the bug fix.
- **No token saving yet:** within +0-6% on three tasks, +21% on the lookup task, where
  reading the map costs more than one direct search. Overall cost +5%.
- **Caveat:** two runs per cell is a small sample, and the user-level `CLAUDE.md` on the test
  machine applied to both setups.


## Run 1: 2026-11-17, Haiku 5.5, 1 repeat, sample shop repo (5 files)
Method: `benchmarks/run_benchmark.py --run --model haiku`. Each task runs on a fresh copy
of `benchmarks/sample_repo`, without and with the kit, same prompt and model, user
settings and MCP servers disabled. Pass/fail comes from hidden checks. Tokens = fresh
input + cache writes + output, subagents included. Total cost of the run: about $0.06.

| Task | Pass (base / kit) | Tokens (base / kit) | Change | Cost $ (base / kit) | Turns (base / kit) |
|---|---|---|---|---|---|
| fix-bug | 1/1 / 1/1 | 16,242 / 19,028 | +17% | 0.0065 / 0.0082 | 9 / 11 |
| add-feature | 1/1 / 1/1 | 13,990 / 17,510 | +25% | 0.0047 / 0.0064 | 6 / 8 |
| locate | 1/1 / 1/1 | 10,261 / 13,761 | +34% | 0.0028 / 0.0039 | 2 / 3 |
| rename* | 1/1 / 1/1 | 16,343 / 20,983 | +28% | 0.0058 / 0.0080 | - |

\* Rerun after fixing a grader bug: the first run's check flagged its own source file.

## What it shows
- **Quality held:** every task passed in both setups, with identical lines changed.
- **On a 5-file project the kit costs more.** Its fixed context (`CLAUDE.md`, learned rules,
  skill descriptions) and the extra turns for reading the map and self-checking outweigh
  any saving. No subagents were used: the tasks were too small to delegate.
- **Not yet shown:** whether savings appear on real-sized projects, where exploratory
  reading dominates. That needs a larger sample repo and 3+ repeats (roadmap item 1).

One run of one repeat on one tiny project is not evidence either way for real projects.

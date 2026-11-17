# Benchmark results

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

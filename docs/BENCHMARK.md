# Benchmark results

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

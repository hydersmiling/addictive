# Benchmark results

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

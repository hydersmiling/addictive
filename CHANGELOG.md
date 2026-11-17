# Changelog

## Unreleased
- **Strict delegation:** the main session only plans, delegates and judges; all reading,
  searching, editing and command runs go to Haiku/Sonnet helpers, however small.
- New `runner` agent (Haiku) for tests and commands.
- Audit benchmark sample (214 files) with planted findings and decoys.

## 1.0.0 (2026-11-17)
First public release.

- **Core kit:** 6 agents (explorer, reviewer, builder, debugger, researcher, big-decision)
  with explicit models and least-privilege tools; 8 skills (compact, lean-code,
  reuse-first, self-check, learn-corrections, map, terse, safe-refactor).
- **Agent catalog:** 198 optional specialists, installed by name, models capped at Sonnet.
- **Optional packs:** code-graph, dev-essentials, llm-compress.
- **Scripts:** code map with secret filtering and staleness check; token counter that
  includes subagents; installer that never overwrites; header checker.
- **Benchmark:** small and large sample projects, hidden graders, token budget cap.
- **Safety:** no hooks, no network access in scripts, privacy guard tests in CI on
  Linux, Windows and macOS.

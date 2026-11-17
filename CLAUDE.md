# Mainseat: project rules

Token-efficient orchestration kit for Claude Code. Recommended main model: **Sonnet**.
Design: `docs/DESIGN.md`. Agents and skills: `.claude/README.md`. Read `docs/LESSONS.md` first.

## How to work here
- Plan with `planner` (Opus) for multi-file or design work; otherwise act directly.
- Reading and searching go to `explorer` (Haiku); tests and commands to `runner` (Haiku);
  diff checks to `reviewer` (Haiku).
- Reuse before creating: map, then `explorer`, then one direct search.
- Code: plain, commented Python, standard library only. Explain steps simply.

## Rules
- No savings claims without a measured benchmark run; record method and numbers in `docs/BENCHMARK.md`.
- Every change reaches `main` through a pull request; CI must pass on Linux, Windows and macOS.
- Third-party files: log every change in `third_party/skills/SOURCE.md`.
- Never commit secrets, session logs or personal details (`tests/test_privacy_guard.py` enforces this).

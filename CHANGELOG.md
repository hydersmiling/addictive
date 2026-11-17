# Changelog

## 1.4.0 (2026-11-17)
- **Installable as a Claude Code plugin:** `claude plugin marketplace add hydersmiling/mainseat`,
  then `claude plugin install mainseat@mainseat`.
- New `/mainseat:setup` skill adds the per-project files (CLAUDE.md, settings, scripts) once.
- Installer `--rules-only` mode for plugin installs.

## 1.3.0 (2026-11-17)
- **Renamed from Tokenwise to Mainseat.** The name says the core idea: the model in the main
  seat sets the price of every turn. The old GitHub address redirects automatically.
  Earlier entries below keep the name the project had at the time.

## 1.2.1 (2026-11-17)
- README: "More than a cost cutter" section describing everything Tokenwise does beyond
  saving tokens, and a one-page visual overview at the top of the page.

## 1.2.0 (2026-11-17)
- **Long-session benchmark:** `--sample session` runs six tasks in one resumed session.
  Result: Sonnet + Tokenwise 6/6 at $0.23 vs plain Opus 6/6 at $0.53 (-57%).
- **Blind quality review run:** Opus reviewer rated plain Opus and Sonnet + Tokenwise as tied
  overall (1 win each, 4 ties); Tokenwise scored higher on keeping to the task.
- **Fix:** if a helper is refused permission, the main session now does the step itself
  instead of stopping (found by the benchmark).
- **Fix:** the judge looks up task text per sample; session costs use the running total.
- Installer ends by recommending a Sonnet main session; README expanded to a full guide
  with a start-here section for new users.

## 1.1.0 (2026-11-17)
- **Blind quality review:** `benchmarks/judge.py` scores baseline vs kit outputs A/B without
  revealing which is which; benchmark runs now record their diff and answer.
- README rewritten around measured results; `.claude/README.md` documents every agent and skill.
- **Recommended setup: Sonnet main session** with Opus only via the new `planner` agent
  (measured -56% cost vs plain Opus, 6/6 passes).
- `measure_tokens.py` shows a token profile: fixed floor, peak context, floor share.
- Benchmark runner: `--kit-model`, `--effort`.
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

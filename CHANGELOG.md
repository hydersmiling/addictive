# Changelog

## 1.7.1 (2026-11-20)
- **IMPORTANT first:** the installed project rules now open with a short IMPORTANT block,
  then who does what, then where to look, so Claude reads the essentials and opens other
  files only when needed. New rule: tests assert exact expected values, never values
  recomputed with the code under test (the one gap a blind review found against Opus).
- The repository's own `CLAUDE.md` follows the same layout, with an index of every doc and
  when to open it, instead of asking Claude to read the lessons file first.

## 1.7.0 (2026-11-20)
- **Split big files safely:** `scripts/find_large.py` lists files over ~400 lines and Python
  functions over ~80; the new `split-file` skill splits them by responsibility and keeps every
  public name importable from its old location (re-exports), with tests before and after.
- **Skills with references:** `split-file` keeps its Python and JavaScript/TypeScript detail in
  `references/` files that load only when needed, following Anthropic's skills guidance.
- **Limits enforced:** `check_agents.py` fails a core skill over 500 lines or with a name and
  description over 1,536 characters; optional third-party skills get a warning.
- **`docs/REFERENCES.md`:** the Anthropic course and docs Mainseat follows, and what it adopts.

## 1.6.2 (2026-11-18)
- Docs: README limits now quote the measured 1.6.0 overhead (+2.5% over plain Sonnet);
  the guide counts four helper scripts; `lean-code` skips the unused-code step when an older
  install lacks the script.

## 1.6.1 (2026-11-18)
- README trimmed from 501 to about 150 lines: install, how it works, results and
  options. The long-form sections moved unchanged to `docs/GUIDE.md`.
- One architecture image (`docs/overview/architecture.svg`): a session's routing and the
  install routes together, plus a short "why it costs less" section.
- **Grows skills:** `learn-corrections` now offers to save a multi-step job taught twice as
  a project skill (user approves; at most 5 learned skills).
- **`scripts/find_unused.py`:** lists Python functions, classes and imports nothing uses, so
  dead code is found without reading every file. Installed with the kit; `lean-code` runs it
  after a change that replaces or removes code.
- **Read once:** the template and `explorer` now say to read only the lines needed, once per
  task, and re-read a file only if it changed.

## 1.6.0 (2026-11-18)
- **Leaner:** every agent and skill description is one line and the template is half as long;
  always-loaded text fell about 61% (1,740 to 690 tokens). Mainseat now costs about the same
  as plain Sonnet (+2.5%, down from +15%).
- **Delegate only when it pays:** small jobs (a known file, a test run, an edit) are done
  directly; helpers handle big searches, noisy commands, large diffs and hard bugs.
- **New `designer` agent (Opus):** builds whole showcase pages in one pass. In blind
  screenshot tests its pages beat plain Opus's (7.9 vs 7.5) at the same cost.
- `scripts/screenshot.py` and `benchmarks/visual_bench.py` for blind visual comparisons.
- Benchmark runs 9-12 published in docs/BENCHMARK.md, including where plain Opus still wins.

## 1.5.0 (2026-11-17)
- **Design work goes to Opus first:** building a new app, page or UI now starts with the
  `planner` writing a design brief (audience, palette, type, layout, copy, no blank image
  placeholders). A side-by-side test showed a Sonnet session designing a whole site alone.
- **Install from a link:** `INSTALL.md` gives any Claude that opens the repository exact
  install steps; the README's first line is the one-line install.

## 1.4.1 (2026-11-17)
- **Fix:** plugin installs now load all 8 core agents. They moved to the root `agents/` folder,
  where Claude Code loads plugin agents; 1.4.0 installed only the skills. Verified with a
  fresh install: 8 agents, 9 skills, about 990 tokens added to each session.

## 1.4.0 (2026-11-17)
- **Installable as a Claude Code plugin:** `claude plugin marketplace add musahyderr/mainseat`,
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

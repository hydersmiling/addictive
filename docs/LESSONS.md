# Lessons

One entry per surprise: what happened, root cause, fix, rule.

## 2026-11-17: third-party builder agent inherited Opus
- What: upstream `builder` has no `model:` line, so it would run on the parent model (Opus).
- Cause: Claude Code uses the parent model when an agent file sets no model.
- Fix: added `model: sonnet`; recorded in `third_party/skills/SOURCE.md`.
- Rule: every agent file in this repo sets `model:` explicitly.

## 2026-11-17: CODEMAP.md listed itself
- What: `--check` always said STALE right after writing the map.
- Cause: the map included its own file, so each write changed the content it compared.
- Fix: the output file is excluded from the list; `--check` also ignores the header's commit hash.
- Rule: a generated file must never describe itself, and freshness checks compare content, not stamps.

## 2026-11-17: "*token*" pattern hid real code
- What: the secret filter would have hidden `measure_tokens.py`.
- Cause: substring patterns match harmless names.
- Fix: whole-name patterns only (`token.json`, `secrets.*`, `credentials*`).
- Rule: match file names exactly or by clear suffix, never by a loose substring.

## 2026-11-17: Windows long paths and duplicate log lines
- What: the token counter found no subagent logs and would have double-counted replies.
- Cause: (1) Claude Code log paths exceed Windows' 260-character limit; `open` and `glob`
  fail or find nothing silently. (2) One reply is written on several lines, each repeating its usage.
- Fix: `\?\` long-path prefix with `os.listdir`; count each (message id, request id) once.
- Rule: test file tools on real Windows paths, and dedupe log records by id before summing.

## 2026-11-17: os.path.relpath crashed across Windows drives
- What: CI on Windows failed: `ValueError: path is on mount 'C:', start on mount 'D:'`.
- Cause: the temp folder was on C: and the repo on D:; Windows has no relative path between drives.
- Fix: catch `ValueError` and fall back to the full path.
- Rule: wrap `relpath` when the two paths can come from different places; CI on Windows catches this.

## 2026-11-17: Bulk rename produced broken words
- What: renaming third-party names with sed turned "caveman-compressed" into "compress-notesed".
- Cause: a short pattern (`caveman-compress`) matched inside a longer word.
- Fix: corrected by hand; grep for every new name after a bulk replace.
- Rule: after any bulk replace, grep the results and read the changed lines before committing.

## 2026-11-17: Agent said "no shell" but had every tool
- What: the third-party builder agent's text said "No Bash available", but its header had no `tools:` line.
- Cause: with no `tools:` line, an agent gets every tool, whatever its instructions say.
- Fix: `tools: Read, Edit, Write, Grep, Glob` on builder; reviewer restricted too.
- Rule: every agent states `tools:` explicitly. Instructions are not permissions.

## 2026-11-17: Benchmark grader failed itself
- What: the rename task failed in both setups on the first real run.
- Cause: `check_rename.py` searched every .py file for `calc_total`, including itself.
- Fix: the check skips its own file; a test now proves it accepts a correct rename.
- Rule: run every grader against a known-good answer before trusting a failure.

## 2026-11-17: The kit cost more on a tiny project
- What: first benchmark: same pass rate, 17-34% more tokens with the kit.
- Cause: fixed context (CLAUDE.md, rules, skill descriptions) plus extra turns; nothing to save on 5 files.
- Rule: report what the data shows; test savings at realistic project size before claiming any.

## 2026-11-17: Review found a fail-open budget and nine smaller risks
- What: the `reviewer` agent (Haiku) found that `--max-tokens` counted an unreadable token
  log as 0, so the budget could never trip; plus JSON parsing of mixed output, symlinks
  followed by the map and installer, BOM-sensitive header checks, and missing key formats.
- Fix: stop when spend is unknown; parse stdout only; skip symlinks; `lexists`; `utf-8-sig`;
  Stripe, Google and JWT patterns; checker refuses to pass when it finds no files.
- Rule: any guard that limits spend or exposure fails closed when its input is missing.

## 2026-11-17: Heredoc turned "\n" into a real line break (twice)
- What: Python edits sent through a bash heredoc broke string literals containing a newline escape.
- Cause: this shell expands the escape before Python sees it.
- Fix: edit such lines with the Edit tool, or build the character with chr(10).
- Rule: never put backslash escapes in code passed through a heredoc on this machine.

## 2026-11-17: Delegating a grep-able search costs more
- What: the one delegated audit run used 2.3x the tokens of a baseline that used grep.
- Rule: delegate reading that needs judgement across many files; let simple pattern
  searches stay a single grep in the main session.

## 2026-11-17: A blocked helper stopped the whole task
- What: in a benchmark run, `runner` (Haiku) was denied permission to run the tests, and the
  Sonnet main session gave up and asked the user instead of running them itself.
- Cause: command permissions granted to the main session did not reach the subagent, and the
  template had no fallback rule.
- Fix: the template now tells the main session to do a refused helper step itself.
- Rule: delegation must degrade gracefully; a blocked helper is never a reason to stop.

## 2026-11-17: Resumed sessions report a running cost total
- What: summing each resumed call's `total_cost_usd` gave session costs about 4x too high.
- Cause: when a session is resumed, Claude Code reports the session's cumulative cost.
- Fix: keep the latest figure, not the sum; costs cross-checked against raw tokens.
- Rule: sanity-check any reported metric against an independent calculation before publishing.

## 2026-11-17: The judge showed the reviewer the wrong task
- What: the first blind review scored correctness 1/10 on tasks both setups had passed.
- Cause: task ids repeat across samples; prompts were looked up by id alone, so large-sample
  pairs got the small sample's task description.
- Fix: prompts keyed by (sample, task id); test added.
- Rule: when a grader's verdict contradicts the hidden tests, suspect the grader first.

## 2026-11-17: Plugin agents in a custom path did not load
- What: v1.4.0 installed cleanly and `claude plugin validate` passed, but `claude plugin details`
  showed Agents (0); the manifest listed the agents under `./.claude/agents/`.
- Cause: in testing, Claude Code loaded plugin agents only from the default `agents/` folder.
- Fix: core agents moved to the root `agents/` folder; the installer copies them into a
  project's `.claude/agents/`; a test pins the location.
- Rule: verify a release by installing it the way a user would, not only by validating it.

## 2026-11-17: PowerShell 5.1 corrupted a UTF-8 file
- What: editing overview.html with `Get-Content | Set-Content` turned ✻, box-drawing
  characters and minus signs into gibberish in the rendered image.
- Cause: Windows PowerShell 5.1 reads files as the ANSI code page unless told otherwise.
- Fix: restored from git and edited with Python using encoding="utf-8".
- Rule: edit text files with Python or the editor, never PowerShell 5.1 Get-Content/Set-Content.

## 2026-11-18: A stale local main made a pull request conflict
- What: a README PR was built on a local `main` four merges behind GitHub; it conflicted,
  and its README and diagrams described an older version of the kit.
- Cause: the branch was cut without fetching first.
- Fix: rebuilt the work on the current `main` in a new PR and closed the stale one.
- Rule: `git fetch` and compare with `origin/main` before cutting a branch or describing the project.

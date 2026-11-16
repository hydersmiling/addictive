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

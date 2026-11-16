# Lessons

One entry per surprise: what happened, root cause, fix, rule.

## 2026-11-17: caveman agent inherited Opus
- What: upstream `cavecrew-builder` has no `model:` line, so it would run on the parent model (Opus).
- Cause: Claude Code uses the parent model when an agent file sets no model.
- Fix: added `model: sonnet`; recorded in `third_party/caveman/SOURCE.md`.
- Rule: every agent file in this repo sets `model:` explicitly.

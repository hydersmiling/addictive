# Tokenwise: project rules

Token-efficient orchestration kit for Claude Code. Design: `docs/DESIGN.md`. Read `docs/LESSONS.md` first.

- Opus plans and judges. Reading and scanning go to `explorer` (Haiku); small edits to `builder`
  (Sonnet); diff checks to `reviewer` (Haiku).
- Reuse before creating: map, then `explorer`, then one direct search.
- Code: plain, commented Python, standard library only. Explain steps simply; the author is learning.
- No savings claims without a measured benchmark run.
- Third-party files: log every change in `third_party/skills/SOURCE.md`.
- Never commit secrets, session logs or personal details (`tests/test_privacy_guard.py` enforces this).

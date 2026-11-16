# Addictive: project rules

Goal: a token-saving "brain" kit for Claude Code. Design: `docs/DESIGN.md`. Research: `docs/RESEARCH.md`.
Read `docs/LESSONS.md` before starting work.

- Opus plans and judges. Delegate finding code to `explorer` / `scout` (Haiku),
  small edits to `builder` (Sonnet), diff checks to `reviewer`.
- Before creating any file or function, check whether it already exists (map, then scout, then one
  direct search). Reuse before you create.
- Code: plain, well-commented Python, standard library only for v1. The author is a beginner:
  explain each step simply.
- Never claim token savings without a measured run. Record method and raw numbers.
- Some skills and agents are third-party (Apache-2.0). Log any change to them in
  `third_party/skills/SOURCE.md`.
- Never commit secrets or session logs.

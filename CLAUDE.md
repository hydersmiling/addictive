# Addictive: project rules

Goal: a token-saving "brain" kit for Claude Code. Design: `docs/DESIGN.md`. Research: `docs/RESEARCH.md`.
Read `docs/LESSONS.md` before starting work.

- Opus plans and judges. Delegate finding code to `caveman-explore` / `cavecrew-investigator` (Haiku),
  small edits to `cavecrew-builder` (Sonnet), diff checks to `cavecrew-reviewer`.
- Before creating any file or function, check whether it already exists (map, then scout, then one
  direct search). Reuse before you create.
- Code: plain, well-commented Python, standard library only for v1. The author is a beginner:
  explain each step simply.
- Never claim token savings without a measured run. Record method and raw numbers.
- `.claude/skills/*` and `.claude/agents/cavecrew-*`, `caveman-explore` come from caveman
  (Apache-2.0). Log any change in `third_party/caveman/SOURCE.md`.
- Never commit secrets or session logs.

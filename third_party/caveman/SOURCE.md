# Caveman: where these files came from

- Upstream: https://github.com/JuliusBrussee/caveman
- Commit: `9b243662ff98d392bc0a95b865a554583d71be75` (2026-11-16), plugin version 4.1.0
- Licence: Apache License 2.0 (copy in `LICENSE`, upstream notice in `NOTICE`).
  Copyright 2026 Julius Brussee. "Caveman" and its rock logo are trademarks of
  Julius Brussee. This project is not affiliated with or endorsed by them.

## Files copied

| Our path | Upstream path | Changed? |
|---|---|---|
| `.claude/skills/caveman/SKILL.md` | `skills/caveman/SKILL.md` | No |
| `.claude/skills/ultracave/SKILL.md` | `skills/ultracave/SKILL.md` | No |
| `.claude/skills/megacave/SKILL.md` | `skills/megacave/SKILL.md` | No |
| `.claude/skills/cavecrew/SKILL.md` | `skills/cavecrew/SKILL.md` | No |
| `.claude/skills/investigate-first/SKILL.md` | `skills/investigate-first/SKILL.md` | No |
| `.claude/skills/lean-build/SKILL.md` | `skills/lean-build/SKILL.md` | No |
| `.claude/skills/surgical-patch/SKILL.md` | `skills/surgical-patch/SKILL.md` | No |
| `.claude/skills/verify-and-stop/SKILL.md` | `skills/verify-and-stop/SKILL.md` | No |
| `.claude/skills/safe-refactor/SKILL.md` | `skills/safe-refactor/SKILL.md` | No |
| `.claude/agents/cavecrew-investigator.md` | `agents/cavecrew-investigator.md` | No |
| `.claude/agents/cavecrew-reviewer.md` | `agents/cavecrew-reviewer.md` | No |
| `.claude/agents/cavecrew-builder.md` | `agents/cavecrew-builder.md` | **Yes**: added `model: sonnet` so edits never run on Opus by default |
| `.claude/agents/caveman-explore.md` | `skills/caveman-explore/SKILL.md` | Moved only: it is written as an agent (has `tools` and `model`), so it lives in `agents/` |

## Not copied, and why

- `caveman-stats`: needs caveman's Node hooks. We will measure with our own script instead.
- `caveman-compress`: sends a file's full text to a model provider through Python scripts.
  Maybe later, after review.
- Hooks, engine, proxy, browse, MCP server: too large for this project, and the hooks
  change behaviour on every prompt.

To update: re-clone upstream, diff against the table above, copy again, and update the commit line.

# Third-party skills: what was copied and changed

Both packs are Apache License 2.0 (see `LICENSE`, and `NOTICE` for authors and links).
Apache-2.0 lets us copy, rename and edit the files as long as we keep the licence and
notices and list our changes. That is what this file does.

## Pack A
Upstream commit `9b243662ff98d392bc0a95b865a554583d71be75` (2026-11-16), version 4.1.0.

| Our path | Upstream path | Changes |
|---|---|---|
| `.claude/skills/terse/SKILL.md` | `skills/caveman/SKILL.md` | Renamed; product name replaced with "terse"; removed mentions of skills we don't ship |
| `.claude/skills/safe-refactor/SKILL.md` | same | None |
| `.claude/agents/builder.md` | `agents/cavecrew-builder.md` | Renamed; names replaced; added `model: sonnet`; added `tools: Read, Edit, Write, Grep, Glob` (the original said it had no shell but granted every tool) |
| `.claude/agents/reviewer.md` | `agents/cavecrew-reviewer.md` | Renamed; names replaced; added `tools: Read, Grep, Glob, Bash` |
| `.claude/agents/explorer.md` | `skills/caveman-explore/SKILL.md` | Renamed; moved to agents (it is written as an agent) |

Removed after review (overlap with our own skills or not useful for beginners):
ultracave, megacave, cavecrew, investigate-first, lean-build, surgical-patch,
verify-and-stop, cavecrew-investigator. See `docs/REVIEW.md`.

Name mapping used: caveman → terse, ultracave → terse-ultra, megacave → terse-classical,
cavecrew → delegate, cavecrew-investigator → scout, cavecrew-builder → builder,
cavecrew-reviewer → reviewer, caveman-explore → explorer.

## Pack B (optional, not installed by default)
Upstream commit `480b61ed91cbc08177dc2c60caa9ffd6c9b95749` (2026-11-16).

| Our path | Upstream path | Changes |
|---|---|---|
| `optional/code-graph/SKILL.md` | `graphify/skill.md` | Skill renamed to `code-graph`; slash command `/graphify` → `/code-graph`; description narrowed so it only triggers on request or when a graph already exists |
| `optional/code-graph/references/*.md` | `graphify/skills/claude/references/*.md` | Slash command renamed as above; heading prefix "graphify reference" → "code-graph reference" |

The skill still calls its command-line tool by its real name, `graphify`, because
that is the program's name. It must be installed separately (`uv tool install graphifyy`).

## Updating
Re-clone upstream, compare with the tables above, copy again, re-apply the changes,
and update the commit lines.

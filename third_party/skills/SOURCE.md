# Third-party skills: what was copied and changed

Licences: packs A, B and D are Apache-2.0, pack C is MIT (see `NOTICE` for authors, links
and which licence file applies). Both licences let us copy, rename and edit the files as
long as we keep the licence and notices; Apache-2.0 also asks us to list our changes.

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
verify-and-stop, cavecrew-investigator. Rationale: `docs/DESIGN.md` (Decisions).

Name mapping used: caveman → terse, ultracave → terse-ultra, megacave → terse-classical,
cavecrew → delegate, cavecrew-investigator → scout, cavecrew-builder → builder,
cavecrew-reviewer → reviewer, caveman-explore → explorer.

## Pack B (optional, not installed by default)
Upstream commit `480b61ed91cbc08177dc2c60caa9ffd6c9b95749` (2026-11-16).

| Our path | Upstream path | Changes |
|---|---|---|
| `optional/code-graph/SKILL.md` | `graphify/skill.md` | Skill renamed to `code-graph`; slash command `/graphify` → `/code-graph`; description narrowed so it only triggers on request or when a graph already exists; extraction subagents told to run on Haiku |
| `optional/code-graph/references/*.md` | `graphify/skills/claude/references/*.md` | Slash command renamed as above; heading prefix "graphify reference" → "code-graph reference" |

The skill still calls its command-line tool by its real name, `graphify`, because
that is the program's name. It must be installed separately (`uv tool install graphifyy`).

## Pack C (optional, not installed by default)
Upstream commit `9c61ab2` (2026-11-08).

| Our path | Upstream path | Changes |
|---|---|---|
| `optional/dev-essentials/debugging-strategies/` | `plugins/developer-essentials/skills/debugging-strategies/` | None |
| `optional/dev-essentials/code-review-excellence/` | `plugins/developer-essentials/skills/code-review-excellence/` | None |
| `optional/dev-essentials/git-advanced-workflows/` | `plugins/developer-essentials/skills/git-advanced-workflows/` | None |
| `optional/dev-essentials/error-handling-patterns/` | `plugins/developer-essentials/skills/error-handling-patterns/` | None |
| `optional/dev-essentials/python-testing-patterns/` | `plugins/python-development/skills/python-testing-patterns/` | None |
| `optional/dev-essentials/javascript-testing-patterns/` | `plugins/javascript-typescript/skills/javascript-testing-patterns/` | None |

## Pack D (optional, not installed by default)
Upstream commit `66e0086` (2026-11-17).

| Our path | Upstream path | Changes |
|---|---|---|
| `optional/llm-compress/SKILL.md` | `skills/headroom/SKILL.md` | Renamed to `llm-compress`; description says it is only for apps that call an LLM API |

The skill tells Claude to add the `headroom-ai` Python/npm package to *your app*. It does
not touch Claude Code. Its separate proxy for coding agents was not included: it routes
your AI traffic through a local server, which is too intrusive for this kit.

## Updating
Re-clone upstream, compare with the tables above, copy again, re-apply the changes,
and update the commit lines.

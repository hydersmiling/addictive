# Inside `.claude`

Everything Claude Code loads from this kit lives here. `scripts/install.py` copies
`agents/`, `skills/`, `settings.json` and `LEARNED.md` into your project's `.claude/`.

## Layout
| Path | What it is | Loaded when |
|---|---|---|
| `agents/*.md` | 8 core subagents (model, tools, instructions) | Description every session; body when called |
| `skills/*/SKILL.md` | 8 core skills | Description every session; body when invoked |
| `settings.json` | Deny rules for secrets, dependencies and build output | Every session |
| `LEARNED.md` | Rules learned from your corrections, imported by `CLAUDE.md` | Every turn |

## Agents
| Agent | Model | Tools | Job |
|---|---|---|---|
| `planner` | Opus | Read, Grep, Glob | Numbered plans for multi-file and design work |
| `explorer` | Haiku | Read, Glob, Grep | All reading and searching; `path:line` answers |
| `runner` | Haiku | Bash, Read | Runs tests and commands; pass/fail + key lines |
| `reviewer` | Haiku | Read, Grep, Glob, Bash | Diff review, one line per finding |
| `builder` | Sonnet | Read, Edit, Write, Grep, Glob | Edits, 1-2 files per call; no shell |
| `debugger` | Sonnet | Read, Grep, Glob, Bash | Root cause before any fix |
| `researcher` | Sonnet | WebSearch, WebFetch, Read, Grep, Glob | Docs and web lookups |
| `big-decision` | Fable | Read, Grep, Glob | Costly-to-reverse decisions |

## Skills
`compact` (reply style), `lean-code`, `reuse-first`, `self-check`, `learn-corrections`,
`map` (`/map`), `terse` (opt-in) and `safe-refactor`.

## Rules for changing these files
- Every agent states `model:` and `tools:` explicitly. An agent with no `tools:` line
  gets every tool, whatever its instructions say.
- Keep descriptions short: they are read in every session.
- Run `python scripts/check_agents.py` after any change; CI runs it too.
- Third-party files (`terse`, `safe-refactor`, `explorer`, `builder`, `reviewer`):
  log every change in `third_party/skills/SOURCE.md`.

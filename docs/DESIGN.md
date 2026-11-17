# Design

## Principle
Spend expensive reasoning only where judgement is needed. Recommended: the main session runs
on Sonnet and calls Opus only through `planner` (measured -56% cost vs plain Opus, equal
quality). If the main session is Opus, it plans,
delegates, judges and answers; it never reads, searches, edits or runs commands itself,
however small the job. Haiku and Sonnet helpers do all hands-on work. Opus tokens cost 40x
Haiku's, so the goal is lower cost per task even if total tokens rise. Quality must hold.

## Roles
| Role | Model | Responsibility | Returns |
|---|---|---|---|
| Main session | Opus | Plan, decide, final check | Decisions |
| `explorer` | Haiku | Big searches (5+ files or long output) | `path:line` list + short answer |
| `runner` | Haiku | Long or noisy commands | pass/fail + key lines |
| `designer` | Opus | Whole pages people will see, in one pass | Finished page |
| `reviewer` | Haiku | Review a diff | One line per finding |
| `builder` | Sonnet | Edits when the main session is Opus | Diff receipt |
| `debugger` | Sonnet | Root cause before any fix | cause / proof / fix |
| `researcher` | Sonnet | Web and docs lookups | Answer + sources |
| `planner` | Opus | Plans multi-file and design work for a cheaper main session | Numbered plan |
| `big-decision` | Fable | Costly-to-reverse choices; two failed attempts | decision / why / risks |
| `make_codemap.py` | none | Build `CODEMAP.md` | File map |

The main session does small jobs itself; helpers are used only when a job is big enough to
repay their start-up cost (measured: delegating small jobs raised cost by 15-48%).

## Mechanisms
- **Code map.** One line per file plus Python symbols; secret files and gitignored paths
  excluded; `--check` detects staleness. Read on demand, never inlined into `CLAUDE.md`.
- **Reuse before create.** Map, then `explorer`, then one direct search, then installed
  dependencies, then `researcher`. A "no match" is always confirmed once.
- **Smallest correct change.** `lean-code` scopes the work to the request and trims the diff.
- **Self-verification.** `self-check` runs the narrowest proof, reads the first error, and
  escalates to `debugger` after two failed fixes.
- **Adaptive rules.** Repeated corrections become one-line rules in `.claude/LEARNED.md`,
  imported by `CLAUDE.md` (40-rule cap, conflicts replaced, no personal data).
- **Shared state through files.** Subagents cannot message each other; they share the map,
  the learned rules and fixed reply formats, so one agent's output feeds the next unchanged.

## Decisions
- **Few skills.** Each skill's description is loaded in every session; overlapping skills
  cost tokens and blur routing. Core kit: 9 skills, 9 agents, one-line descriptions. Specialised packs are optional.
- **Least privilege.** Every agent declares `tools:` and `model:` explicitly. Instructions
  are not permissions.
- **Nothing implicit.** No hooks, no network access in scripts, no overwriting user files.
- **Measured claims only.** The benchmark records tokens (subagents included), cost,
  pass/fail from hidden checks, and lines changed. A saving that lowers the pass rate is a loss.

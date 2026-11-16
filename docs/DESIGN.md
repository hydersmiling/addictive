# Design

## Principle
Spend expensive reasoning only where judgement is needed. Opus plans and decides;
cheaper models read, search and make routine edits; a generated map replaces
exploratory file reads. Every saving must hold output quality constant.

## Roles
| Role | Model | Responsibility | Returns |
|---|---|---|---|
| Main session | Opus | Plan, decide, final check | Decisions |
| `explorer` | Haiku | All reading and scanning: locate code, answer "does this exist?" | `path:line` list |
| `reviewer` | Haiku | Review a diff | One line per finding |
| `builder` | Sonnet | Edits of 1-2 files | Diff receipt |
| `debugger` | Sonnet | Root cause before any fix | cause / proof / fix |
| `researcher` | Sonnet | Web and docs lookups | Answer + sources |
| `big-decision` | Fable | Costly-to-reverse choices; two failed attempts | decision / why / risks |
| `make_codemap.py` | none | Build `CODEMAP.md` | File map |

The main session reads code only to judge it, never to find it.

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
  cost tokens and blur routing. Core kit: 8 skills, 6 agents. Specialised packs are optional.
- **Least privilege.** Every agent declares `tools:` and `model:` explicitly. Instructions
  are not permissions.
- **Nothing implicit.** No hooks, no network access in scripts, no overwriting user files.
- **Measured claims only.** The benchmark records tokens (subagents included), cost,
  pass/fail from hidden checks, and lines changed. A saving that lowers the pass rate is a loss.

# Addictive

A starter kit that sets Claude Code up to work smart and waste fewer tokens.
Made for people who have just installed Claude Code.

- **A team instead of one expensive model.** Your main session (Opus) plans and decides.
  Cheaper helpers do the legwork: Haiku finds code, Sonnet edits, debugs and researches.
  Fable is called only for the biggest, hard-to-undo decisions.
- **A code map.** `CODEMAP.md` lists every file with a one-line summary, so Claude can
  find code without opening dozens of files.
- **Reuse before you create.** Claude checks whether something exists before writing it.
- **Short replies.** The [caveman](https://github.com/JuliusBrussee/caveman) skills cut filler,
  never code or facts.
- **Real numbers.** A script reads Claude Code's own logs to show what a session cost.

> **Status: v1, not yet benchmarked.** We make no token-saving claims until the benchmark
> in [docs/ROADMAP.md](docs/ROADMAP.md) is done. Measure your own sessions with
> `measure_tokens.py`.

## Quick start (5 minutes)
You need Python 3.9+ and git.

```bash
git clone https://github.com/hydersmiling/addictive
python addictive/scripts/install.py path/to/your-project --dry-run
python addictive/scripts/install.py path/to/your-project
```

Then, in your project:
1. Open `CLAUDE.md` and fill in the two lines at the top.
2. Build the map: `python scripts/make_codemap.py`
3. Start Claude Code. Type `/caveman` for short replies, `/map` to refresh the map.
4. After a session: `python scripts/measure_tokens.py` to see the real token counts.

The installer never overwrites your files. It lists anything it skipped.

## What's in the kit

| Piece | What it does |
|---|---|
| `scripts/make_codemap.py` | Writes `CODEMAP.md`. Skips gitignored files and secrets. `--check` tells you if it's stale. |
| `scripts/measure_tokens.py` | Sums tokens per model from your local session logs, subagents included. Sends nothing anywhere. |
| `scripts/install.py` | Copies the kit into a project without overwriting anything. |
| `scripts/check_agents.py` | Catches typos in agent headers (a typo can silently run an agent on your priciest model). |
| `CLAUDE.md.template` | Short project rules: who does what, reuse-before-create, how to debug. |
| `.claude/settings.json` | Stops Claude reading `.env`, keys, `node_modules`, build output and lock files. |
| `docs/token-tips.md` | Habits that save the most tokens. |

### Agents
| Agent | Model | Job |
|---|---|---|
| `caveman-explore`, `cavecrew-investigator` | Haiku | Find where code lives; answer "do we have this already?" |
| `cavecrew-builder` | Sonnet | Small edits to 1-2 files, renames |
| `cavecrew-reviewer` | Haiku | Check a diff, one line per issue |
| `debugger` | Sonnet | Reproduce a bug and find the root cause before any fix |
| `researcher` | Sonnet | Web and docs lookups, short answer with sources |
| `big-decision` | Fable | Rare: architecture, data model, security design, or after two failed attempts |

No Fable access? Change `model: fable` to `model: opus` in `.claude/agents/big-decision.md`.

### Skills
`caveman`, `ultracave`, `megacave` (short-reply modes), `cavecrew` (when to delegate),
`investigate-first`, `lean-build`, `surgical-patch`, `safe-refactor`, `verify-and-stop`
(working styles), and `map` (refresh the code map).

## Honest limits
- **Subagents aren't free.** Each one starts with its own context. They save tokens only
  when they read a lot and return a little. See [docs/token-tips.md](docs/token-tips.md).
- **Deny rules aren't a security wall.** Some Claude Code versions have had bugs where deny
  rules didn't apply inside subagents. Keep real secrets out of your project folder.
- **The map's summaries are short.** They come from docstrings, top comments and headings.
  Files without those get a name only.
- **Tested with:** Claude Code as of November 2026. Agent and settings formats change;
  CI checks the headers.

## How it's designed
[docs/DESIGN.md](docs/DESIGN.md) covers the roles, the map, the reuse gate and how quality
is kept. [docs/RESEARCH.md](docs/RESEARCH.md) covers related projects and why we chose this
approach.

## Credits and licence
Our code is MIT ([LICENSE](LICENSE)). Skills and four agents come from
[caveman](https://github.com/JuliusBrussee/caveman) by Julius Brussee, Apache-2.0. See
[third_party/caveman/SOURCE.md](third_party/caveman/SOURCE.md) for exactly what was copied
and changed. Not affiliated with or endorsed by the caveman project.

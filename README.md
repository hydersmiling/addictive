# Addictive

A starter kit that sets Claude Code up to work smart and waste fewer tokens.
Made for people who have just installed Claude Code.

- **A team instead of one expensive model.** Your main session (Opus) plans and decides.
  Cheaper helpers do the legwork: Haiku finds code, Sonnet edits, debugs and researches.
  Fable is called only for the biggest, hard-to-undo decisions.
- **A code map.** `CODEMAP.md` lists every file with a one-line summary, so Claude finds
  code without opening dozens of files. Big project? Add the optional code graph.
- **Reuse before you create.** Claude searches the map, scouts and dependencies before
  writing new code.
- **Smallest correct change.** Only what you asked, checked before it's called done.
- **Debugs itself.** Runs the check, reads the first error, and after two failed fixes
  hands over to a debugger agent instead of guessing.
- **Learns your corrections.** Correct the same thing twice and it becomes a lasting rule
  in `.claude/LEARNED.md`.
- **Short replies.** `/terse` cuts filler, never code or facts.
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
3. Start Claude Code. `/terse` for short replies, `/map` to refresh the map, `/learn <rule>` to teach a rule.
4. After a session: `python scripts/measure_tokens.py` to see the real token counts.

The installer never overwrites your files. It lists anything it skipped.
Large codebase? Add `--with-code-graph` (also needs `uv tool install graphifyy`).

## What's in the kit

| Piece | What it does |
|---|---|
| `scripts/make_codemap.py` | Writes `CODEMAP.md`. Skips gitignored files and secrets. `--check` tells you if it's stale. |
| `scripts/measure_tokens.py` | Sums tokens per model from your local session logs, subagents included. Sends nothing anywhere. |
| `scripts/install.py` | Copies the kit into a project without overwriting anything. |
| `scripts/check_agents.py` | Catches typos in agent headers (a typo can silently run an agent on your priciest model). |
| `CLAUDE.md.template` | Short project rules: who does what, and the rules for every change. |
| `.claude/LEARNED.md` | Rules Claude has learned from your corrections. Edit freely. |
| `.claude/settings.json` | Stops Claude reading `.env`, keys, `node_modules`, build output and lock files. |
| `docs/token-tips.md` | Habits that save the most tokens. |
| `docs/MCP.md` | Which MCP servers are worth their token cost. |

### Agents
| Agent | Model | Job |
|---|---|---|
| `explorer`, `scout` | Haiku | Find where code lives; answer "do we have this already?" |
| `builder` | Sonnet | Small edits to 1-2 files, renames |
| `reviewer` | Haiku | Check a diff, one line per issue |
| `debugger` | Sonnet | Reproduce a bug and find the root cause before any fix |
| `researcher` | Sonnet | Web and docs lookups, short answer with sources |
| `big-decision` | Fable | Rare: architecture, data model, security design, or after two failed attempts |

No Fable access? Change `model: fable` to `model: opus` in `.claude/agents/big-decision.md`.

### Skills
| Skill | Use |
|---|---|
| `lean-code` | Smallest correct change; only what was asked |
| `reuse-first` | Search before creating any file, function or dependency |
| `self-check` | Prove it works; debug failures; escalate after two tries |
| `learn-corrections` | Turn repeated corrections into rules (`/learn`) |
| `map` | Refresh the code map (`/map`) |
| `terse`, `terse-ultra`, `terse-classical` | Short-reply modes |
| `delegate` | When to hand work to which agent |
| `investigate-first`, `lean-build`, `surgical-patch`, `safe-refactor`, `verify-and-stop` | Working styles for debugging, features, fixes, refactors and final checks |
| `code-graph` (optional) | Knowledge graph for large codebases |

## Honest limits
- **Subagents aren't free.** Each one starts with its own context. They save tokens only
  when they read a lot and return a little. See [docs/token-tips.md](docs/token-tips.md).
- **"Shorter code" is an instruction, not a guarantee.** The reviewer and the benchmark
  check it; nothing forces it.
- **Deny rules aren't a security wall.** Some Claude Code versions have had bugs where deny
  rules didn't apply inside subagents. Keep real secrets out of your project folder.
- **The optional code graph** sends docs, PDFs and images (not code) to Google Gemini
  if a Gemini API key is set on your machine. Code itself is parsed locally.
- **Tested with:** Claude Code as of November 2026. Agent and settings formats change;
  CI checks the headers.

## How it's designed
[docs/DESIGN.md](docs/DESIGN.md) covers the roles, the map, reuse-first, learning and how
quality is kept. [docs/RESEARCH.md](docs/RESEARCH.md) covers related projects.

## Licence
Our code is MIT ([LICENSE](LICENSE)). Some skills and agents are third-party, under the
Apache License 2.0; see [third_party/skills/](third_party/skills/) for the licence,
notices and every change we made.

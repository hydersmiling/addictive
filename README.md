# Tokenwise

Token-efficient orchestration for Claude Code. Tokenwise routes work by cognitive
demand: Opus reasons and decides, Sonnet executes, Haiku reads and retrieves. A
secret-aware codebase map replaces exploratory file reads, a reuse-before-create
discipline prevents duplicate code, and every change is self-verified before it is
reported. Rules learned from your corrections persist across sessions.

> **Status:** v1. Savings are not yet benchmarked, so none are claimed.

## Install
Requires Python 3.9+ and git.
```bash
git clone https://github.com/hydersmiling/tokenwise
python tokenwise/scripts/install.py path/to/project --dry-run
python tokenwise/scripts/install.py path/to/project
```
Then fill in the two lines at the top of `CLAUDE.md` and run `python scripts/make_codemap.py`.
The installer never overwrites existing files.

Optional packs: `--with code-graph dev-essentials llm-compress`.

## Agents
| Agent | Model | Role |
|---|---|---|
| `explorer` | Haiku | All reading and scanning; returns `path:line` only |
| `reviewer` | Haiku | Diff review, one line per finding; cannot edit |
| `builder` | Sonnet | Edits of 1-2 files; no shell |
| `debugger` | Sonnet | Reproduces failures and isolates the root cause |
| `researcher` | Sonnet | Documentation and web lookups with sources |
| `big-decision` | Fable | Rare: architecture, data model, security design, or after two failed attempts |

No Fable access: set `model: opus` in `.claude/agents/big-decision.md`.

## Skills
| Skill | Purpose |
|---|---|
| `compact` | Default reply style: the answer, then at most one short follow-up |
| `lean-code` | Smallest correct change, scoped to the request |
| `reuse-first` | Search map, agents and dependencies before creating anything |
| `self-check` | Verify every change; escalate to `debugger` after two failed fixes |
| `learn-corrections` | Turn repeated corrections into persistent rules (`/learn`) |
| `map` | Refresh `CODEMAP.md` (`/map`) |
| `terse` | Opt-in: maximally short replies |
| `safe-refactor` | Restructure without changing behaviour |

Optional: `code-graph` (knowledge graph for large repositories), `dev-essentials`
(debugging, code review, git, error handling, Python and JS testing), `llm-compress`
(context compression for applications that call an LLM API).

## Tools
| Script | Purpose |
|---|---|
| `scripts/make_codemap.py` | Generate `CODEMAP.md`; `--check` reports staleness |
| `scripts/measure_tokens.py` | Token use per model from local session logs, subagents included |
| `scripts/check_agents.py` | Validate agent and skill headers |
| `benchmarks/run_benchmark.py` | Compare runs with and without the kit (dry run by default) |

## Benchmark
Four fixed tasks (fix a bug, add a feature, locate code, rename a symbol) run on two
copies of a sample project, with and without the kit, using the same model and prompt.
It records tokens, cost, lines changed, and pass/fail from hidden checks. A saving
counts only if the pass rate holds. A real run (`--run`) uses your Claude plan or API credit.

## Privacy
Scripts make no network calls. No hooks, no permission bypass, least-privilege agents.
Secret files are excluded from the map and denied to Claude. CI fails on committed
emails, personal paths or keys. See [docs/PRIVACY.md](docs/PRIVACY.md).

## Documentation
[Design](docs/DESIGN.md) · [Token tips](docs/token-tips.md) · [MCP servers](docs/MCP.md) ·
[Privacy](docs/PRIVACY.md) · [Roadmap](docs/ROADMAP.md) · [Lessons](docs/LESSONS.md)

## License
MIT. Third-party skills keep their licences (Apache-2.0 or MIT); see
[third_party/skills](third_party/skills/).

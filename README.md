# Tokenwise

A verified collection of 200+ specialized Claude Code subagents and 16 skills for
token-efficient development: 6 core agents installed by default and a catalog of 198
specialists you add by name.

Tokenwise routes work by cognitive demand: Opus reasons and decides, Sonnet executes,
Haiku reads and retrieves, and Fable is reserved for rare, costly-to-reverse decisions.
A secret-aware codebase map replaces exploratory file reads. A reuse-before-create
discipline searches the map, scout agents and installed dependencies before any new
code is written. Every change is scoped to the request, verified by the narrowest
passing check, and escalated to a debugger after two failed fixes instead of looping.
Corrections you repeat become persistent project rules, so you teach each preference
once. Replies are compact: the answer, then at most one short follow-up.

**Verified:** every agent and skill header is validated in CI, and 30 tests run on
Linux, Windows and macOS. Privacy guards fail the build on network access in scripts,
hooks, permission bypasses, committed emails, personal paths or keys.

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
Catalog agents: `--list-agents`, then `--agents security-auditor backend-architect ...`.

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

**Agent catalog (optional, 198 agents).** Specialists for languages, frameworks,
infrastructure, security, data, testing, documentation and more, capped at Sonnet or
Haiku for cost. Install only the ones you need: each installed agent's description is
read in every session.

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

**Results so far** ([details](docs/BENCHMARK.md)): on a 64-file project with Opus, every task
passed with and without the kit (16/16). The kit changed far fewer lines (7 vs 23.5 on the
feature task), cost about the same (+5% overall), and did not yet reduce tokens. On a
5-file project it cost 17-34% more. The template has since been trimmed.

## Privacy
Scripts make no network calls. No hooks, no permission bypass, least-privilege agents.
Secret files are excluded from the map and denied to Claude. CI fails on committed
emails, personal paths or keys. See [docs/PRIVACY.md](docs/PRIVACY.md).

## Documentation
[Design](docs/DESIGN.md) · [Benchmark](docs/BENCHMARK.md) · [Token tips](docs/token-tips.md) · [MCP servers](docs/MCP.md) ·
[Privacy](docs/PRIVACY.md) · [Roadmap](docs/ROADMAP.md) · [Lessons](docs/LESSONS.md)

## License
MIT. Third-party skills keep their licences (Apache-2.0 or MIT); see
[third_party/skills](third_party/skills/).

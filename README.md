# Tokenwise

A verified collection of 200+ specialized Claude Code subagents and 16 skills for
token-efficient development: 8 core agents installed by default and a catalog of 198
specialists you add by name.

Tokenwise routes work by cognitive demand: Opus only plans, delegates and judges; every
hands-on step, however small, goes to Sonnet (edits, debugging, research) or Haiku
(reading, searching, running tests). Fable is reserved for rare, costly-to-reverse decisions.
A secret-aware codebase map replaces exploratory file reads. A reuse-before-create
discipline searches the map, scout agents and installed dependencies before any new
code is written. Every change is scoped to the request, verified by the narrowest
passing check, and escalated to a debugger after two failed fixes instead of looping.
Corrections you repeat become persistent project rules, so you teach each preference
once. Replies are compact: the answer, then at most one short follow-up.

**Verified:** every agent and skill header is validated in CI, and 30 tests run on
Linux, Windows and macOS. Privacy guards fail the build on network access in scripts,
hooks, permission bypasses, committed emails, personal paths or keys.

## Recommended: run the main session on Sonnet
```bash
claude --model sonnet        # or type /model sonnet inside Claude Code
```
Every reply of the main session re-reads its whole context at the main model's price,
so the main model is the biggest cost lever. Sonnet runs the session, Haiku helpers read
and run tests, and Opus is called only through the `planner` agent for real design work.
Measured on 6 tasks: **Sonnet + kit cost 56% less than plain Opus, and every task passed
in both** (6/6). The kit also produced the smallest change on the feature task (6 lines,
vs 22 for plain Opus). Plain Sonnet was cheaper still (-64%); the kit's rules add about
22% on short tasks. Details: [docs/BENCHMARK.md](docs/BENCHMARK.md).

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
| `explorer` | Haiku | All reading and searching; returns `path:line` and a short answer |
| `runner` | Haiku | Runs tests and commands; reports pass/fail and key lines |
| `reviewer` | Haiku | Diff review, one line per finding; cannot edit |
| `builder` | Sonnet | Every edit, 1-2 files per call; no shell |
| `debugger` | Sonnet | Reproduces failures and isolates the root cause |
| `researcher` | Sonnet | Documentation and web lookups with sources |
| `planner` | Opus | Plans multi-file work, design and unclear fixes; called by a cheaper main session |
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

**Results so far** ([details](docs/BENCHMARK.md)): quality held in every valid run (44/44 graded passes
across four runs). With strict delegation on Opus, helpers did all hands-on work and Opus
took 65% fewer turns, but total cost rose 25% on short single tasks, because each Opus
session has a fixed token floor and helper tokens add to it. It cost less only on the
largest task (-14%). Long multi-task sessions, where savings should appear, are not yet measured.

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

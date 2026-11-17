# Tokenwise

**Opus-quality results at Sonnet prices.** Tokenwise sets up Claude Code so a mid-price
model runs your session, cheap helpers do the reading, and Opus steps in only to plan.
Same passing result, about half the cost, smaller diffs.

| Measured on the same tasks | Plain Opus | Sonnet + Tokenwise |
|---|---|---|
| Tasks passed (hidden graders) | 10/10 | **10/10** |
| Cost, 6 real-size tasks | $1.12 | **$0.49 (-56%)** |
| Cost, 4 small tasks | $0.59 | **$0.33 (-44%)** |
| Lines changed, feature task | 22 | **6** |

86 graded benchmark runs so far, every one passed. Method and raw numbers: [docs/BENCHMARK.md](docs/BENCHMARK.md).

## Start in one minute
```bash
git clone https://github.com/hydersmiling/tokenwise
python tokenwise/scripts/install.py path/to/project
claude --model sonnet          # run your session on Sonnet
```
Fill in the two lines at the top of the new `CLAUDE.md`, then run `python scripts/make_codemap.py`.
The installer never overwrites your files.

## Who does what
| Role | Model | Why |
|---|---|---|
| Main session: understands, decides, edits known files | **Sonnet** | Every reply re-reads the whole context, so this seat sets the price |
| `planner`: designs multi-file work | Opus | Strongest reasoning, used only when a plan is needed |
| `explorer`, `runner`, `reviewer`: read, search, run tests, review | Haiku | 40x cheaper than Opus for mechanical work |
| `builder`, `debugger`, `researcher`: edits, root causes, docs lookups | Sonnet | Capable and half Opus's price |
| `big-decision`: costly-to-reverse choices | Fable | Rare; falls back to Opus if unavailable |

Why Opus doesn't build: building is many turns of reading and editing, and every turn is
paid at the session model's price. Opus earns its cost on the plan, not the keystrokes.

## What to use
| You want | Use |
|---|---|
| Opus-level results for less | `claude --model sonnet` + Tokenwise |
| The lowest possible cost on simple work | `claude --model haiku` + Tokenwise (passed every small task, $0.02 for four) |
| A hard design or architecture call | Let the session call `planner` or `big-decision` |
| A large codebase | `--with code-graph` |

## What you get
- **Code map:** one-line summary of every file; secrets and ignored files left out.
- **Reuse before create:** searches the map and existing helpers before writing new code.
- **Smallest correct change:** only what you asked for, verified by the narrowest test.
- **Self-debugging:** two failed fixes hand over to a debugger instead of looping.
- **Learns your corrections:** say it twice and it becomes a rule in `.claude/LEARNED.md`.
- **Compact replies:** the answer, then at most one short follow-up.
- **200+ agents:** 8 core plus 198 optional specialists (`--list-agents`, `--agents NAME`).
- **Real numbers:** `scripts/measure_tokens.py` shows any session's tokens, subagents included.

## Honest limits
- Quality is graded by hidden tests and checks: correctness and reuse. Code style is not scored.
- Most savings come from Sonnet as the main model. Plain Sonnet was cheaper still (-64%);
  the kit's rules cost about 20-30% on short tasks and buy smaller, reused, checked changes.
- One or two runs per setup so far. Long multi-task sessions are not yet measured.

## Safe by design
No hooks, no network calls in scripts, no permission bypass, least-privilege agents.
CI on Linux, Windows and macOS fails on leaked emails, personal paths or keys.
`main` is protected: every change goes through a pull request with passing checks.

[Design](docs/DESIGN.md) · [Benchmark](docs/BENCHMARK.md) · [Token tips](docs/token-tips.md) ·
[MCP](docs/MCP.md) · [Privacy](docs/PRIVACY.md) · [Roadmap](docs/ROADMAP.md) · [Changelog](CHANGELOG.md)

MIT licence. Third-party skills keep their licences; see [third_party/skills](third_party/skills/).

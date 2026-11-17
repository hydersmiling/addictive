# Tokenwise

**Opus-quality results at Sonnet prices.** Tokenwise reorganises Claude Code around a
simple economic insight: the model that *runs* your session sets the price of every
turn, so that seat should be held by a capable mid-price model, while the most
expensive reasoning is reserved for the moments that genuinely require it. Sonnet
conducts, Haiku reads, Opus plans. The result is the same passing work for roughly
half the cost, delivered in smaller, cleaner changes.

> **Recommended:** run your main session on **Sonnet** (`claude --model sonnet`).
> Tokenwise calls Opus for you, through its `planner` agent, only when a plan is needed.

| Measured on identical tasks | Plain Opus | Sonnet + Tokenwise |
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
claude --model sonnet
```
Fill in the two lines at the top of the new `CLAUDE.md`, then run `python scripts/make_codemap.py`.
The installer never overwrites your files.

## The thesis
Most advice on saving tokens targets the wrong variable. Every reply in a Claude Code
session re-reads a fixed floor of context (system prompt, tool definitions, project
instructions and skill descriptions), typically 12,000 to 14,000 tokens, plus the
conversation so far. That floor is charged at the main model's rate, on every turn,
for the whole session. Shortening a prompt saves pennies; choosing who sits in the main
seat changes the bill by a factor. Tokenwise is built on that observation and on a
second one: an expensive model's judgement is worth paying for, but its keystrokes are not.

## Anatomy of a request
1. **Understand.** Sonnet reads your request and the project's rules.
2. **Locate.** For anything beyond a known file, a Haiku `explorer` consults the code map
   and returns precise `path:line` citations, keeping bulky reading out of the main context.
3. **Plan.** If the work spans several files or needs design, the Opus `planner` returns a
   short numbered plan, then steps back.
4. **Build.** Sonnet makes the smallest change that fully satisfies the request, reusing
   existing helpers before writing new ones.
5. **Verify.** A Haiku `runner` executes the narrowest test that proves the change; two
   failed fixes escalate to a `debugger` instead of looping.
6. **Learn.** If you correct the same thing twice, it becomes a lasting rule.

## Who does what
| Role | Model | Why |
|---|---|---|
| Main session: understands, decides, edits known files | **Sonnet** | Every reply re-reads the whole context, so this seat sets the price |
| `planner`: designs multi-file work | Opus | Strongest reasoning, used only when a plan is needed |
| `explorer`, `runner`, `reviewer`: read, search, run tests, review | Haiku | 40x cheaper than Opus for mechanical work |
| `builder`, `debugger`, `researcher`: edits, root causes, docs lookups | Sonnet | Capable at half Opus's price |
| `big-decision`: costly-to-reverse choices | Fable | Rare; falls back to Opus if unavailable |

**Why doesn't Opus build?** Building is many turns of reading and editing, each paid at the
session model's price. Opus earns its cost on the plan, not on the keystrokes.

## What to use
| You want | Use |
|---|---|
| Opus-level results for less | `claude --model sonnet` + Tokenwise |
| The lowest cost on simple work | `claude --model haiku` + Tokenwise (passed every small task: $0.02 for four) |
| A hard design or architecture call | Let the session call `planner` or `big-decision` |
| A large codebase | `install.py --with code-graph` |

## Design principles
- **Spend judgement, not attention.** Expensive models decide; cheap models fetch.
- **Measure, never assume.** No claim ships without a benchmark run behind it.
- **Least privilege.** Every agent declares its model and tools; readers cannot edit,
  editors have no shell.
- **Nothing implicit.** No hooks, no background network calls, no overwritten files.
- **Small by default.** Fewer skills, shorter rules, smaller diffs: every line in the
  main context is paid for again on every turn.

## What you get
- **Code map:** a one-line summary of every file; secrets and ignored files left out.
- **Reuse before create:** searches the map and existing helpers before writing new code.
- **Smallest correct change:** only what you asked for, verified by the narrowest test.
- **Self-debugging:** two failed fixes hand over to a debugger instead of looping.
- **Learns your corrections:** say it twice and it becomes a rule in `.claude/LEARNED.md`.
- **Compact replies:** the answer, then at most one short follow-up.
- **200+ agents:** 8 core plus 198 optional specialists (`--list-agents`, `--agents NAME`).
- **Real numbers:** `scripts/measure_tokens.py` profiles any session: tokens per model,
  subagents included, and how much of it was the fixed floor.

## How we measure
Each benchmark task runs on two fresh copies of a sample project, one plain and one with
Tokenwise, under identical flags, with personal settings and MCP servers disabled.
Correctness is judged by hidden checks copied in only after Claude finishes, so they
cannot be gamed; audit tasks also plant decoys that must *not* be reported. Tokens come
from Claude Code's own logs, subagents included. A saving counts only if the pass rate
holds. A blind A/B review (`benchmarks/judge.py`) scores readability and fit with the
codebase without telling the reviewer which setup produced which change.

## Honest limits
- Most of the saving comes from Sonnet in the main seat; plain Sonnet was cheaper still
  (-64%). Tokenwise's rules cost about 20-30% on short tasks and buy smaller, reused,
  verified changes.
- One or two runs per setup so far; long multi-task sessions are not yet measured.
- Code style is scored by the blind review, which has not yet been run on recorded outputs.

## Safe by design
No hooks, no network calls in scripts, no permission bypass, least-privilege agents.
CI on Linux, Windows and macOS fails on leaked emails, personal paths or keys.
`main` is protected: every change goes through a pull request with passing checks.

[Design](docs/DESIGN.md) · [Benchmark](docs/BENCHMARK.md) · [Token tips](docs/token-tips.md) ·
[MCP](docs/MCP.md) · [Privacy](docs/PRIVACY.md) · [Roadmap](docs/ROADMAP.md) · [Changelog](CHANGELOG.md) ·
[Inside .claude](.claude/README.md)

MIT licence. Third-party skills keep their licences; see [third_party/skills](third_party/skills/).

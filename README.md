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
| Long session, 6 tasks in one conversation | $0.53 | **$0.23 (-57%)** |
| Blind code review (6 pairs, Opus as reviewer) | 1 win | **1 win, 4 ties** |

101 graded benchmark runs so far; one failed, exposing a defect that is now fixed. Method and raw numbers: [docs/BENCHMARK.md](docs/BENCHMARK.md).

## Start in one minute
```bash
git clone https://github.com/hydersmiling/tokenwise
python tokenwise/scripts/install.py path/to/project
claude --model sonnet
```
Fill in the two lines at the top of the new `CLAUDE.md`, then run `python scripts/make_codemap.py`.
The installer never overwrites your files.

## New to Claude Code? Start here
If you have just installed Claude Code, Tokenwise gives you a sound configuration on day
one, so you never have to learn the expensive habits first. Five steps:

1. **Install the kit into your project.** Run the installer shown above. It adds a short
   `CLAUDE.md`, the agents and skills, and two helper scripts. Nothing you already have is
   replaced.
2. **Describe your project in two lines.** Open `CLAUDE.md` and fill in what the project is
   and the command that runs its tests. Claude reads this on every turn, so two precise
   lines are worth more than a page of background.
3. **Build the code map.** `python scripts/make_codemap.py` writes `CODEMAP.md`, a one-line
   summary of every file. Claude consults it instead of opening files at random.
4. **Start on Sonnet.** `claude --model sonnet`. This single choice delivers most of the
   saving. You do not need to call Opus yourself; the kit's `planner` does that when a task
   genuinely needs a plan.
5. **Work normally.** Ask for what you want in plain language. Tokenwise decides who reads,
   who builds and who checks, and replies with the answer and at most one short follow-up.

After your first few sessions, run `python scripts/measure_tokens.py` to see what they
actually cost. Most new users are surprised by how much of a session is the fixed floor,
and by how much shorter sessions on a mid-price model reduce it.

### Choosing a model: a field guide
Start every session on **Sonnet**. It handles everyday building, debugging and refactoring
with the same graded pass rate as Opus in our benchmarks, at roughly half the price per
token. Move to **Haiku** (`/model haiku`) for routine, well-specified work: renames, small
fixes, documentation edits, test runs. It passed every small benchmark task for a few cents.
Reach for **Opus** directly only when a whole session is design work, such as an
architecture review or a difficult migration; for a single hard decision inside an ordinary
session, let the `planner` or `big-decision` agent handle it. Switching costs nothing, so
the right habit is to match the model to the next stretch of work, not to the most
difficult moment you can imagine.

### Writing requests that cost less
The cheapest token is the one never needed. A few habits make every model more efficient:

- **Name what you know.** "Fix the rounding in `apply_discount` in `orders/pricing.py`"
  lets Claude open one file; "something is wrong with prices" makes it search.
- **Paste the decisive line, not the log.** One error line and its file reference say more
  than two hundred lines of output.
- **State the finish line.** "Done when the pricing tests pass" stops work at the right
  moment instead of inviting polish.
- **One topic per session.** Start fresh with `/clear` when you change subject; a long
  session re-reads its entire history on every reply.
- **Ask for a plan on large changes.** Correcting a plan is cheaper than correcting code.

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

## The economics, worked through
Consider a modest task that takes twenty replies in the main session. If each reply
re-reads a 13,000-token floor before anything else, the session has read 260,000 tokens
of fixed context alone, before counting the conversation, the files opened, or the
answer written. Prompt caching softens this, because repeated context is billed at a
fraction of the fresh-input rate, but the fraction is still charged at the main model's
price. Moving the main seat from Opus to Sonnet halves the price of every one of those
twenty re-reads. Delegating bulk reading to Haiku removes those pages from the main
context altogether, so they are never re-read at all.

This is why Tokenwise treats model choice as architecture rather than preference. An
expensive model in the main seat pays premium rates for routine turns: listing files,
reading a function, running a test, confirming an edit landed. Each turn is cheap in
isolation and costly in aggregate. A capable mid-price model handles those turns just as
reliably, and the benchmark shows it: Sonnet in the main seat passed every graded task
that Opus passed. Opus is kept for planning, where depth of reasoning changes the outcome.

There is a second, quieter saving. Smaller changes are cheaper to review, cheaper to
test, and less likely to break something that needs fixing in a later session. On the
feature task, Tokenwise produced a 6-line change where plain Opus wrote 22. That
difference does not appear on the bill, but it compounds over the life of a codebase.

## Walkthroughs
**Fixing a failing test.** You write: "the test suite fails, fix it." Sonnet asks the
Haiku `runner` to run the suite, which returns only the decisive lines: one failing test
and its assertion. Sonnet opens the file the traceback names, finds the off-by-one in a
discount threshold, corrects one line, and asks `runner` to confirm the suite passes.
If the first fix had failed and the second had too, the `debugger` would have been asked
for a root cause instead of a third guess. You receive one sentence naming the cause and
the fix, and a one-line follow-up if there is anything left to decide.

**Adding a feature.** You ask for a function that summarises an order as text. Before
writing anything, Tokenwise's reuse discipline searches the code map and existing modules,
finds the money-formatting helper and the order-total function, and builds the summary on
top of them. The result is a few lines that read like the rest of the codebase, rather
than a fresh implementation of currency formatting that someone must later reconcile.

**Auditing a large codebase.** You ask which files build SQL by inserting values into a
query string. If a single search pattern answers it, Sonnet runs that search itself; if
the question needs judgement across many files, a Haiku `explorer` reads them and returns
citations, and Sonnet checks the cited lines before answering. In the benchmark's audit
tasks, Tokenwise found every planted problem and reported none of the correct look-alikes.

## The agents in depth
- **`planner` (Opus).** Receives a goal, constraints and relevant locations, reads only
  what it needs, and returns at most eight concrete steps plus a check command. It never
  edits. If the goal is ambiguous it asks one question rather than guessing.
- **`explorer` (Haiku).** The kit's eyes. It searches in parallel, cites only line ranges
  it actually read, and answers in `path:line` form so its findings can be verified quickly.
- **`runner` (Haiku).** Runs tests, builds and read-only commands, and reports pass or
  fail with at most ten key lines. It refuses installs, pushes, deletions and deployments.
- **`builder` (Sonnet).** Makes edits of one or two files per call, re-reads its work to
  verify it, and returns a short receipt. It has no shell, by design.
- **`reviewer` (Haiku).** Reviews a diff and reports one finding per line with severity
  and a suggested fix. It cannot edit, so a review never silently becomes a rewrite.
- **`debugger` (Sonnet).** Reproduces a failure, separates symptom from cause, ranks
  hypotheses by evidence, and returns the cause, the proof and the smallest fix.
- **`researcher` (Sonnet).** Looks up documentation and current versions, summarises in
  its own words with sources, and never sends your code or personal details to a search.
- **`big-decision` (Fable).** Consulted rarely: architecture, data models, security design,
  or a problem that cheaper agents have failed twice. It returns a decision, its reasons,
  its risks and the rejected options.

Beyond these eight, an optional catalog of 198 specialists covers languages, frameworks,
infrastructure, security, data and documentation. Each is capped at Sonnet or Haiku and
installed only by name, because every installed agent's description is read in every session.

## The skills in depth
- **`compact`** sets the reply style: the answer in plain sentences, then at most one short
  follow-up. It expands automatically for security warnings, irreversible actions, or a
  confused reader.
- **`lean-code`** restates the request in one line, treats everything outside it as out of
  scope, and trims the diff before declaring the work done.
- **`reuse-first`** searches the map, the codebase and installed dependencies, in that
  order, before anything new is created, and records the decision as reuse, extend or new.
- **`self-check`** runs the narrowest proof first, reads the first error rather than the
  last, and escalates after two failed attempts.
- **`learn-corrections`** turns a repeated correction into a one-line rule in
  `.claude/LEARNED.md`, replaces conflicting rules, and refuses to store personal details.
- **`map`** refreshes `CODEMAP.md`. **`terse`** is an opt-in mode for maximally short
  replies. **`safe-refactor`** restructures code while proving behaviour is unchanged.

## Installation options
```bash
python scripts/install.py PATH --dry-run              # preview; changes nothing
python scripts/install.py PATH                        # core kit
python scripts/install.py PATH --with dev-essentials  # debugging, review, git and testing skills
python scripts/install.py PATH --with code-graph      # knowledge graph for large repositories
python scripts/install.py --list-agents               # browse the 198 catalog agents
python scripts/install.py PATH --agents security-auditor backend-architect
```
The installer copies files and never overwrites one you already have; anything skipped is
listed so you can merge it by hand. It finishes by recommending a Sonnet main session.

## Measuring your own sessions
```bash
python scripts/measure_tokens.py              # the latest session in this folder
python scripts/measure_tokens.py --last 5     # the last five
```
The report lists tokens per model, subagents included, and a profile of the main session:
how many replies it made, the fixed floor each reply re-read, the peak context, and what
share of everything read was that floor. When the floor dominates, the remedy is fewer
main-session replies or a cheaper main model, not a shorter prompt. Everything is read
from Claude Code's local logs; nothing leaves your machine.

## Customising Tokenwise
- **Project rules** live in `CLAUDE.md`. Keep it short: it is read on every turn.
- **Learned rules** live in `.claude/LEARNED.md`. Edit or delete them freely.
- **Models** are set per agent in the `model:` line of each file in `.claude/agents/`.
  Without Fable access, set `big-decision` to `opus`.
- **New agents** must declare `model:` and `tools:`; run `python scripts/check_agents.py`
  to catch typos, which Claude Code would otherwise ignore silently.

## Benchmark history
Eight runs so far, each published with its method and caveats in
[docs/BENCHMARK.md](docs/BENCHMARK.md). Early runs on a five-file project showed the kit's
overhead outweighing any saving, which led to a leaner template. A 64-file project
confirmed equal quality with much smaller diffs. Search-heavy audits on a 214-file
project showed that delegating a search one pattern can answer costs more, which changed
the delegation rules. Strict delegation from an Opus main session cut Opus turns by 65%
but raised cost, which pointed to the main seat as the real lever. Comparing main models
directly then showed Sonnet with Tokenwise passing everything plain Opus passed for
44-56% less. A long six-task session confirmed it (-57%), and a blind review by Opus
rated the two setups' code as tied overall.

## FAQ
**Does Tokenwise make Claude worse?** In 101 graded runs, every setup passed the same tasks
apart from one run that exposed a since-fixed defect. A blind code review scored the two
setups as tied overall: 1 win each, 4 ties.

**Why not run everything on Haiku?** You can, for simple work, and it is remarkably cheap.
For ambiguous requests and design decisions, Sonnet's and Opus's judgement is worth the price.

**Do I need Fable?** No. `big-decision` falls back to Opus with a one-line change.

**Will it change my files during installation?** It only adds files that do not exist yet.

**Does it send my code anywhere?** The scripts make no network calls. Claude Code itself
talks to Anthropic as usual; the optional code graph can use Google Gemini for documents
only if you have set a Gemini key.

**Why are some savings negative?** On very small tasks, the kit's own instructions cost
more than they save. The benchmark reports this rather than hiding it.

**Can I use it with an existing CLAUDE.md?** Yes. The installer skips it, and you can merge
the template's sections by hand.

**How do I switch the main model mid-session?** Type `/model sonnet` (or `opus`, `haiku`)
inside Claude Code. The change applies from the next reply; your conversation is kept.

**How often should I start a fresh session?** Whenever you switch to unrelated work. A
fresh session starts from the floor alone, while a long one re-reads its whole history on
every reply. `/clear` resets it; `/compact` replaces the history with a summary.

## Troubleshooting
- **An agent never gets used:** check its file with `python scripts/check_agents.py`; a
  misspelled header field is ignored without warning.
- **The map seems out of date:** `python scripts/make_codemap.py --check` says whether it
  is stale; `/map` rebuilds it.
- **Costs are higher than expected:** run `measure_tokens.py` and look at the floor share;
  a long session or an expensive main model is the usual cause.

## Who it's for
Tokenwise suits anyone who uses Claude Code often enough for the bill or the usage limit
to matter: solo developers on a subscription who keep hitting their weekly cap, teams who
want predictable spend across many sessions, and newcomers who would rather start from a
sound, measured configuration than assemble one by trial and error. It assumes nothing
beyond Python 3.9 and git, and it never asks you to change how you describe your work.

## Security model
The kit is designed so that installing it cannot quietly widen what Claude can do. No
file in it runs automatically: there are no hooks, so nothing executes on your prompts,
commits or sessions. The helper scripts import no networking libraries, and a test fails
the build if one ever does. Agents declare their tools explicitly, so a reader cannot
edit, an editor cannot open a shell, and a reviewer cannot rewrite what it reviews. Deny
rules keep Claude away from environment files, keys, credentials, dependency folders and
build output, although secrets belong outside the project folder in any case. The code
map leaves out files that look like secrets and drops any summary line that resembles a
password or token. Third-party skills and agents are pinned to a recorded upstream
commit, with every local change listed beside it.

## Glossary
- **Main session:** the conversation you type into; its model sets the price of every reply.
- **Subagent:** a helper with its own context, model and tools, called by the main session.
- **Fixed floor:** the context every reply re-reads before your conversation begins.
- **Cache read:** context billed at a reduced rate because it was sent recently.
- **Code map:** `CODEMAP.md`, a one-line summary of every file in the project.
- **Hidden check:** a test copied in only after Claude finishes, so it cannot be gamed.
- **Decoy:** a correct file planted beside a flawed one, to catch over-reporting.

## Working in a team
Tokenwise is plain files in your repository, so it travels with the code. Commit
`CLAUDE.md`, `.claude/agents`, `.claude/skills` and `.claude/settings.json`, and every
teammate's Claude Code session follows the same routing, the same reply style and the same
safety rules. `.claude/LEARNED.md` can be shared as well: a correction one person teaches
becomes a rule for everyone, which is often the fastest way to encode a team's conventions.
Review changes to these files the way you review code, because they shape how every
session behaves. Keep personal preferences in your own user-level settings instead, so the
shared configuration stays focused on the project.

## Upgrading and removing
To upgrade, pull the latest Tokenwise and run the installer again. It adds new files and
skips existing ones, so local edits are never overwritten; compare any skipped file with
the new version and merge what you want. To remove Tokenwise, delete the files it added:
the agents and skills in `.claude/`, `.claude/LEARNED.md`, `CODEMAP.md`, and the two
scripts in `scripts/`. Remove or edit `CLAUDE.md` and `.claude/settings.json` if you have
not customised them. Nothing else on your system is touched, because nothing else was ever
installed.

## Known trade-offs
Every design choice here buys something and costs something, and it is better to know both.
The kit's instructions are read on every turn, which adds a small fixed cost that only pays
for itself once tasks involve real reading, reuse or verification. Delegating to helpers
keeps the main context lean, but a helper repeats some orientation work, so delegating a
search that one pattern could answer costs more than doing it directly. Strict scoping
produces smaller changes, which occasionally means Claude asks before extending a task you
half-expected it to extend. The benchmark tasks are deliberately controlled; your own
codebase is the final arbiter, and `measure_tokens.py` exists so that you can check.

### When Tokenwise is not the right tool
If you use Claude Code only occasionally, for a quick question or a single small edit,
the kit's instructions will cost more than they save, and a plain Sonnet session is the
better choice. The same is true for one-off scripts in a throwaway folder. Tokenwise earns
its keep in projects you return to: codebases with history, conventions and tests, where
reuse, verification and remembered corrections compound from one session to the next. If
your work is mostly long design conversations rather than code changes, running Opus
directly for those sessions remains perfectly reasonable; the kit simply makes sure you
are not paying Opus rates for the routine turns around them.

## A tour of the repository
| Path | Purpose |
|---|---|
| `CLAUDE.md.template` | The short project rules the installer copies into your project |
| `.claude/agents/` | The eight core agents, each with an explicit model and tool list |
| `.claude/skills/` | The eight core skills, loaded only when relevant |
| `optional/` | The agent catalog and optional skill packs, installed only on request |
| `scripts/` | Installer, code map, token counter and header checker, all standard-library Python |
| `benchmarks/` | Sample projects, task definitions, hidden graders, the runner and the blind judge |
| `tests/` | Unit tests, including privacy guards that run on every push |
| `docs/` | Design notes, benchmark results, token tips, privacy and lessons learned |
| `third_party/` | Licences, notices and the change log for every borrowed file |

## Judging the savings yourself
Benchmarks describe controlled tasks; your work is not controlled. The most reliable test
is a simple before-and-after on your own project. Pick a task you do often, such as
fixing a failing test or adding a small endpoint. Do it once in a plain session on your
usual model and once on Sonnet with Tokenwise installed, with the same request. After each,
run `python scripts/measure_tokens.py` and note the tokens per model and the floor share.
Then compare the two results the way a reviewer would: does each change work, is it the
right size, does it reuse what already exists? If the cheaper setup produced equally good
work, the saving is real for you. If it did not, the numbers will tell you where it went,
and the [design notes](docs/DESIGN.md) explain which part of the kit to adjust.

## More questions
**Is Tokenwise a plugin?** Not yet. It is a set of plain files you install with one
command, which keeps everything visible and editable. Plugin packaging is on the roadmap.

**Does it work with any programming language?** The agents, skills and routing are
language-neutral. The code map summarises every file and lists function and class names
for Python today; other languages get one-line summaries without symbols.

**What happens on a subscription plan?** You are not billed per token, but usage limits
are measured in the same tokens. Lower usage means more work before a limit is reached.

**Why are the replies so short?** The `compact` style answers first and stops. Ask "why"
or "explain" and it expands; security warnings and irreversible actions are always
explained in full.

**Can I turn individual features off?** Yes. Delete an agent or skill file, or remove a
rule from `CLAUDE.md`. Nothing depends on anything hidden.

## What comes next
The next milestones are repeated runs to tighten the error bars, symbol extraction for more
languages in the code map, a one-command health check for an installed project, trimming the
kit's per-turn instructions so it costs less over plain Sonnet, and packaging as a Claude Code
plugin. Each will ship the way everything here has: with its method and its numbers.

## Credits
Tokenwise builds on the work of several open-source projects, whose skills and agents are
included under their original licences and credited in
[third_party/skills](third_party/skills/), together with a list of every local change. It
also owes its method to a simple discipline: measure before claiming, and publish the
numbers, including the unflattering ones. Suggestions, issues and benchmark results from
your own projects are warmly welcomed.

## Contributing
Every change reaches `main` through a pull request, and CI must pass on Linux, Windows and
macOS. Keep the code plain, commented Python with no dependencies. Back any savings claim
with a benchmark run and record its method in `docs/BENCHMARK.md`.

## Honest limits
- Most of the saving comes from Sonnet in the main seat; plain Sonnet was cheaper still
  (-64%). Tokenwise's rules cost about 20-30% on short tasks and buy smaller, reused,
  verified changes.
- One or two runs per setup so far, so treat the percentages as indicative.
- In the blind review the two setups tied overall; plain Opus was slightly stronger on
  correctness details (8.8 vs 8.5), Tokenwise on keeping to the task (10 vs 8.7).

## Safe by design
No hooks, no network calls in scripts, no permission bypass, least-privilege agents.
CI on Linux, Windows and macOS fails on leaked emails, personal paths or keys.
`main` is protected: every change goes through a pull request with passing checks.

[Design](docs/DESIGN.md) · [Benchmark](docs/BENCHMARK.md) · [Token tips](docs/token-tips.md) ·
[MCP](docs/MCP.md) · [Privacy](docs/PRIVACY.md) · [Roadmap](docs/ROADMAP.md) · [Changelog](CHANGELOG.md) ·
[Inside .claude](.claude/README.md)

MIT licence. Third-party skills keep their licences; see [third_party/skills](third_party/skills/).

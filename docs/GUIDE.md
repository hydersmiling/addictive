# Mainseat guide

The long-form companion to the [README](../README.md): why the kit is built this way, how to get the most from it, and answers to common questions.

## More than a cost cutter
Lower cost is the headline, but the everyday difference is a Claude that behaves like a
disciplined senior engineer: it stays on task, builds on what already exists, proves its
work, remembers how you like things done, and keeps out of what it should not touch.

| Capability | What it means for you |
|---|---|
| **Precise, minimal changes** | Claude does exactly what was asked, in the fewest lines that fully solve it. In the benchmarks its changes were about a third the size of plain Opus's (22 lines against 60) for identical results, which makes every change faster to review and safer to ship. |
| **Reuse before reinvention** | Before writing anything new, Mainseat checks whether the project already has it, then reuses or extends that code. Duplicate helpers, the slow tax on every growing codebase, are stopped before they are written. |
| **Self-verifying work** | Every change is proven by the narrowest test that demonstrates it. If a fix fails twice, the problem is handed to a dedicated debugger for a root-cause analysis instead of a third guess. |
| **An assistant that learns** | Correct Claude twice on the same point, or say "always" or "never", and the preference becomes a one-line project rule. Every future session follows it without being told again. |
| **Instant orientation** | The code map summarises every file in a single line, so Claude, and every new teammate, can see what lives where without opening the codebase file by file. |
| **Security by construction** | Environment files, keys and credentials are kept out of Claude's reach and out of the map. Each helper agent receives only the tools its role requires, nothing runs in the background, and the installer never overwrites a file. |
| **Expertise on demand** | A catalog of 198 specialist agents, covering security, databases, frontend, infrastructure and more, ready to add by name whenever a project calls for depth. |
| **Replies that respect your time** | The answer comes first, followed by at most one short next step. No preamble, no recap, and full explanation whenever a risk or an irreversible action is involved. |
| **Shared team standards** | Commit the configuration and every teammate's Claude follows the same routing, rules and safeguards. A correction one person teaches can become a convention for the whole team. |
| **Evidence you can reproduce** | `measure_tokens.py` reveals what any session truly cost, and the benchmark with its blind reviewer lets you compare any two setups on your own tasks, so no claim has to be taken on trust. |

## New to Claude Code? Start here
If you have just installed Claude Code, Mainseat gives you a sound configuration on day
one, so you never have to learn the expensive habits first. Five steps:

1. **Install the kit into your project.** Run the installer shown above. It adds a short
   `CLAUDE.md`, the agents and skills, and four helper scripts. Nothing you already have is
   replaced.
2. **Describe your project in two lines.** Open `CLAUDE.md` and fill in what the project is
   and the command that runs its tests. Claude reads this on every turn, so two precise
   lines are worth more than a page of background.
3. **Build the code map.** `python scripts/make_codemap.py` writes `CODEMAP.md`, a one-line
   summary of every file. Claude consults it instead of opening files at random.
4. **Start on Sonnet.** `claude --model sonnet`. This single choice delivers most of the
   saving. You do not need to call Opus yourself; the kit's `planner` does that when a task
   genuinely needs a plan.
5. **Work normally.** Ask for what you want in plain language. Mainseat decides who reads,
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
seat changes the bill by a factor. Mainseat is built on that observation and on a
second one: an expensive model's judgement is worth paying for, but its keystrokes are not.

## Anatomy of a request
1. **Understand.** Sonnet reads your request and the project's rules.
2. **Locate.** Sonnet opens files it already knows. For searches across many files, a Haiku `explorer` consults the code map
   and returns precise `path:line` citations, keeping bulky reading out of the main context.
3. **Plan.** If the work spans several files or needs design, the Opus `planner` returns a
   short numbered plan, then steps back.
4. **Build.** Sonnet makes the smallest change that fully satisfies the request, reusing
   existing helpers before writing new ones.
5. **Verify.** Sonnet runs the narrowest test that proves the change (a Haiku `runner` handles long, noisy commands); two
   failed fixes escalate to a `debugger` instead of looping.
6. **Learn.** If you correct the same thing twice, it becomes a lasting rule.

## Design principles
- **Spend judgement, not attention.** Expensive models decide; cheap models fetch.
- **Measure, never assume.** No claim ships without a benchmark run behind it.
- **Least privilege.** Every agent declares its model and tools; readers cannot edit,
  editors have no shell.
- **Nothing implicit.** No hooks, no background network calls, no overwritten files.
- **Small by default.** Fewer skills, shorter rules, smaller diffs: every line in the
  main context is paid for again on every turn.

## How we measure
Each benchmark task runs on two fresh copies of a sample project, one plain and one with
Mainseat, under identical flags, with personal settings and MCP servers disabled.
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

This is why Mainseat treats model choice as architecture rather than preference. An
expensive model in the main seat pays premium rates for routine turns: listing files,
reading a function, running a test, confirming an edit landed. Each turn is cheap in
isolation and costly in aggregate. A capable mid-price model handles those turns just as
reliably, and the benchmark shows it: Sonnet in the main seat passed every graded task
that Opus passed. Opus is kept for planning, where depth of reasoning changes the outcome.

There is a second, quieter saving. Smaller changes are cheaper to review, cheaper to
test, and less likely to break something that needs fixing in a later session. On the
feature task, Mainseat produced a 6-line change where plain Opus wrote 22. That
difference does not appear on the bill, but it compounds over the life of a codebase.

## Walkthroughs
**Fixing a failing test.** You write: "the test suite fails, fix it." Sonnet asks the
test suite itself and reads only the decisive lines: one failing test
and its assertion. Sonnet opens the file the traceback names, finds the off-by-one in a
discount threshold, corrects one line, and re-runs the suite to confirm it passes.
If the first fix had failed and the second had too, the `debugger` would have been asked
for a root cause instead of a third guess. You receive one sentence naming the cause and
the fix, and a one-line follow-up if there is anything left to decide.

**Adding a feature.** You ask for a function that summarises an order as text. Before
writing anything, Mainseat's reuse discipline searches the code map and existing modules,
finds the money-formatting helper and the order-total function, and builds the summary on
top of them. The result is a few lines that read like the rest of the codebase, rather
than a fresh implementation of currency formatting that someone must later reconcile.

**Auditing a large codebase.** You ask which files build SQL by inserting values into a
query string. If a single search pattern answers it, Sonnet runs that search itself; if
the question needs judgement across many files, a Haiku `explorer` reads them and returns
citations, and Sonnet checks the cited lines before answering. In the benchmark's audit
tasks, Mainseat found every planted problem and reported none of the correct look-alikes.

## The agents in depth
- **`planner` (Opus).** Receives a goal, constraints and relevant locations, reads only
  what it needs, and returns at most eight concrete steps plus a check command. It never
  edits. If the goal is ambiguous it asks one question rather than guessing.
- **`designer` (Opus).** Designs and builds a whole page people will see in one pass: a
  detailed hero visual, one memorable showpiece section and specific copy, with no blank
  placeholders. In blind tests its pages beat plain Opus's at the same cost.
- **`explorer` (Haiku).** The kit's eyes for big searches. It searches in parallel, cites only line ranges
  it actually read, and answers in `path:line` form so its findings can be verified quickly.
- **`runner` (Haiku).** Runs long or noisy commands, and reports pass or
  fail with at most ten key lines. It refuses installs, pushes, deletions and deployments.
- **`builder` (Sonnet).** For an Opus main session only: makes edits of one or two files per call, re-reads its work to
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

Beyond these nine, an optional catalog of 198 specialists covers languages, frameworks,
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

## Benchmark history
Eight runs so far, each published with its method and caveats in
[BENCHMARK.md](BENCHMARK.md). Early runs on a five-file project showed the kit's
overhead outweighing any saving, which led to a leaner template. A 64-file project
confirmed equal quality with much smaller diffs. Search-heavy audits on a 214-file
project showed that delegating a search one pattern can answer costs more, which changed
the delegation rules. Strict delegation from an Opus main session cut Opus turns by 65%
but raised cost, which pointed to the main seat as the real lever. Comparing main models
directly then showed Sonnet with Mainseat passing everything plain Opus passed for
44-56% less. A long six-task session confirmed it (-57%), and a blind review by Opus
rated the two setups' code as tied overall.

## FAQ
**Does Mainseat make Claude worse?** In 131 graded runs, every setup passed the same tasks
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

## More questions
**Is Mainseat a plugin?** Not yet. It is a set of plain files you install with one
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

## Troubleshooting
- **An agent never gets used:** check its file with `python scripts/check_agents.py`; a
  misspelled header field is ignored without warning.
- **The map seems out of date:** `python scripts/make_codemap.py --check` says whether it
  is stale; `/map` rebuilds it.
- **Costs are higher than expected:** run `measure_tokens.py` and look at the floor share;
  a long session or an expensive main model is the usual cause.

## Who it's for
Mainseat suits anyone who uses Claude Code often enough for the bill or the usage limit
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
Mainseat is plain files in your repository, so it travels with the code. Commit
`CLAUDE.md`, `.claude/agents`, `.claude/skills` and `.claude/settings.json`, and every
teammate's Claude Code session follows the same routing, the same reply style and the same
safety rules. `.claude/LEARNED.md` can be shared as well: a correction one person teaches
becomes a rule for everyone, which is often the fastest way to encode a team's conventions.
Review changes to these files the way you review code, because they shape how every
session behaves. Keep personal preferences in your own user-level settings instead, so the
shared configuration stays focused on the project.

## Upgrading and removing
To upgrade, pull the latest Mainseat and run the installer again. It adds new files and
skips existing ones, so local edits are never overwritten; compare any skipped file with
the new version and merge what you want. To remove Mainseat, delete the files it added:
the agents and skills in `.claude/`, `.claude/LEARNED.md`, `CODEMAP.md`, and the four
scripts in `scripts/` (`make_codemap.py`, `measure_tokens.py`, `screenshot.py`, `find_unused.py`, `find_large.py`). Remove or edit `CLAUDE.md` and `.claude/settings.json` if you have
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

### When Mainseat is not the right tool
If you use Claude Code only occasionally, for a quick question or a single small edit,
the kit's instructions will cost more than they save, and a plain Sonnet session is the
better choice. The same is true for one-off scripts in a throwaway folder. Mainseat earns
its keep in projects you return to: codebases with history, conventions and tests, where
reuse, verification and remembered corrections compound from one session to the next. If
your work is mostly long design conversations rather than code changes, running Opus
directly for those sessions remains perfectly reasonable; the kit simply makes sure you
are not paying Opus rates for the routine turns around them.

## Judging the savings yourself
Benchmarks describe controlled tasks; your work is not controlled. The most reliable test
is a simple before-and-after on your own project. Pick a task you do often, such as
fixing a failing test or adding a small endpoint. Do it once in a plain session on your
usual model and once on Sonnet with Mainseat installed, with the same request. After each,
run `python scripts/measure_tokens.py` and note the tokens per model and the floor share.
Then compare the two results the way a reviewer would: does each change work, is it the
right size, does it reuse what already exists? If the cheaper setup produced equally good
work, the saving is real for you. If it did not, the numbers will tell you where it went,
and the [design notes](DESIGN.md) explain which part of the kit to adjust.

# Addictive: design

## The idea in one line
A "brain" for Claude Code: Opus thinks and decides, Sonnet and Haiku do the
reading, renaming and routine edits, and a **code tree** (map) lets everyone find
things without opening files, so we spend as few tokens as possible.

## Who does what

| Role | Model | Jobs | Returns |
|---|---|---|---|
| **Brain** (main session) | Opus | Understand the request, plan, choose files, judge hard trade-offs, final check | Decisions and plans |
| **Scout** (`caveman-explore`, `cavecrew-investigator`) | Haiku | Find where things live, answer "do we already have X?" | `path:line` list only |
| **Builder** (`cavecrew-builder`) | Sonnet | Edits of 1-2 files, renames, mechanical changes | Short diff receipt |
| **Reviewer** (`cavecrew-reviewer`) | Haiku, upgrade to Sonnet for risky code | Check a diff | One line per issue |
| **Debugger** (`debugger`) | Sonnet | Root cause of bugs, before any fix | cause, proof, smallest fix |
| **Researcher** (`researcher`) | Sonnet | Web and docs lookups | short answer + sources |
| **Big decision** (`big-decision`) | Fable (optional) | Only choices that are expensive to undo, or after two failed attempts | decision, why, risks |
| **Mapper** (`scripts/make_codemap.py`, plain Python, no model) | none | Build and refresh the tree | `CODEMAP.md` |

Rule: the brain never reads a whole file to *find* something; it asks the scout or
the map. The brain reads code only when it must *judge* it.

## The tree (CODEMAP.md)
- Folder tree + one line per file + function/class names (v2).
- Header holds the git commit hash; `--check` warns when the map is stale.
- Skips `.gitignore`d files and anything that looks like a secret.
- CLAUDE.md has only a one-line pointer to it, so it costs tokens only when read.

## "Check before you create" (reuse gate)
Before making a new file, function or module:
1. Search the map for the name and close synonyms (exact whole-word match, then fuzzy).
2. If unsure, ask the scout: "Is there already code that does X?" It returns `path:line` or `No match.`
3. Found → extend or reuse it. Not found → create, then refresh the map.
4. Never trust a `No match.` blindly: do one targeted search yourself first (caveman's own rule).

This is the cheapest place to save tokens *and* avoid duplicate code.

## Keeping the result as good as "Opus does everything"
Cheaper models only help if the final result is the same. So the agents must also:

1. **Fixed output contracts.** Every subagent answers in a fixed shape (`path:line — note`,
   diff receipt, `No match.`). The brain can check the shape and spot a bad answer at once.
2. **Evidence, not opinions.** Scouts cite line ranges they actually read. Line numbers
   past the end of a file are rejected.
3. **Escalate instead of guessing.** Builder replies `too-big.`, `ambiguous.` or
   `needs-confirm.` and stops; the brain then decides. Haiku tasks that fail twice move to
   Sonnet; Sonnet tasks that fail twice return to Opus.
4. **Verify every change.** Builder re-reads what it wrote; reviewer checks the diff; tests
   run before "done" (`verify-and-stop` skill).
5. **Keep the map honest.** Refresh after every new file; refuse to use a stale map.
6. **Measure both cost and quality.** The benchmark runs the same tasks with and without
   Addictive and records tokens *and* whether the task passed (tests green, same files
   changed). A token saving that lowers the pass rate is a loss, not a win.
7. **Count subagent tokens too.** Subagents have their own context; their logs live in
   `<session>/subagents/*.jsonl`. Leaving them out would fake the savings.
8. **Plain English when it matters.** Caveman voice drops to normal sentences for security
   warnings, irreversible actions and questions to the user.

## v1 scope (from the brief, adjusted by research)
1. `scripts/make_codemap.py`: tree + summaries + commit hash + `--check`, secret-safe.
2. Agents: the four caveman agents above, plus an `Explore` override on Haiku.
3. `CLAUDE.md.template` under ~80 lines with the reuse-gate rule and map pointer.
4. `.claude/settings.json` deny rules (secrets, node_modules, build output), documented
   as a helper only: deny rules may not apply inside subagents.
5. `scripts/measure_tokens.py`: reads session JSONL including subagents.
6. README with measured results only.

Later: symbol-aware map (tree-sitter), doctor script, `/map` command, hooks, plugin packaging.

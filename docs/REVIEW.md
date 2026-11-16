# Professional review (2026-11-17)

How an experienced engineer would judge this kit, and what changed because of it.

## Principles they would apply
1. **Every skill and agent costs tokens in every session.** Claude Code loads each one's
   `description` up front so it knows when to use it. Ten overlapping skills cost more
   than three clear ones, and they confuse the model about which to pick.
2. **One job, one tool.** If two skills say the same thing, delete one.
3. **Least privilege.** An agent gets only the tools its job needs. An agent that edits
   files doesn't need a shell.
4. **Nothing runs by surprise.** No hooks, no network calls from scripts, no files changed
   without the user asking.
5. **Claims need numbers.** Ship the benchmark; report ranges and the method.

## What was removed
| Removed | Why |
|---|---|
| `terse-ultra`, `terse-classical` skills | Two more versions of the short-reply mode; one uses classical Chinese. Too much for beginners. `compact` (default) and `terse` (opt-in) cover it. |
| `delegate` skill | 3.8 KB of routing rules that repeat the "Who does what" section of `CLAUDE.md`, and it pointed to agents we removed. |
| `scout` agent | Same job as `explorer` (Haiku, read-only, `path:line` answers). Two agents for one job make Claude pick at random. |
| `lean-build`, `surgical-patch` skills | Covered by `lean-code`. |
| `verify-and-stop` skill | Covered by `self-check`. |
| `investigate-first` skill | Covered by the `debugger` agent plus `self-check`. |

Result: 15 skills down to 8, 7 agents down to 6.

## What was fixed
| Change | Why |
|---|---|
| `builder` now has `tools: Read, Edit, Write, Grep, Glob` | Its instructions said "no Bash available", but with no `tools:` line it could run any command. A safety bug inherited from the source. |
| `reviewer` now has `tools: Read, Grep, Glob, Bash` | A reviewer must never edit. Bash stays for `git diff`. |
| New default reply style `compact` | The answer in plain sentences plus at most one short follow-up. Clearer than terse fragments for new users. |

## What they would still recommend (not done yet)
1. **Run the benchmark** on the sample repo and one real repo, and put the numbers in the README.
2. **Rename the project.** "Addictive" doesn't say what it does. See the name ideas below.
3. **A `doctor` script** that checks the setup and prints fixes (roadmap item 2).
4. **Version the kit** (tags + CHANGELOG) so users know what changed when they update.
5. **Keep `CLAUDE.md.template` under 40 lines.** It's read on every turn.

## Name ideas
- **Tokenwise** (recommended): says what it does, short, easy to search.
- **Lean Brain**: matches the "brain with helpers" design.
- **Sparecode**: fewer tokens, less code.
Avoid putting "Claude" in the name: it's Anthropic's trademark.
Check that the name is free on GitHub and PyPI before renaming.

# Privacy and safety

What the kit does with your code and data, in plain words.

## The scripts
| Script | Reads | Writes | Network |
|---|---|---|---|
| `make_codemap.py` | File names and the first lines of files git tracks | `CODEMAP.md` only | None |
| `measure_tokens.py` | Claude Code's local logs in `~/.claude/projects` | Nothing (prints to screen) | None |
| `install.py` | The kit's own files | New files in your project; **never overwrites** | None |
| `check_agents.py` | The kit's agent and skill files | Nothing | None |
| `run_benchmark.py` | The sample repo | Throwaway copies in your temp folder, deleted after | Runs `claude -p`, only with `--run` |

A test (`tests/test_privacy_guard.py`) fails the build if any of these scripts ever
imports a network library.

## Secrets
- `make_codemap.py` leaves out files that look like secrets (`.env`, keys, credentials) by
  name, and drops any summary line that looks like a password or token.
- `.claude/settings.json` asks Claude Code not to read those files. Some Claude Code
  versions have had bugs where this didn't apply inside subagents, so **keep real secrets
  out of your project folder** (use environment variables or a secrets manager).

## The agents and skills
- No hooks: nothing runs automatically on your prompts, commits or sessions.
- No permission bypass anywhere. Claude Code still asks you before risky actions.
- Agents get only the tools their job needs: `explorer` can only read; `builder` can edit
  but has no shell; `reviewer` can't edit.
- The `researcher` agent searches the web. Its instructions forbid putting your code,
  file contents, names or personal details into a search.
- `.claude/LEARNED.md` stores rules only. The skill that writes it refuses personal
  details and secrets, because the file may be committed.

## The optional code graph
Installed only with `--with-code-graph`. Code is parsed on your machine. Docs, PDFs and
images are summarised by your Claude session, **or sent to Google Gemini if a
`GEMINI_API_KEY`/`GOOGLE_API_KEY` is set**. It can also clone GitHub repos you ask it to,
and its `hooks` option can add a git hook. Use it only on request.

## This repository
A test fails if a commit adds an email address (other than GitHub noreply or example
addresses), a personal folder path, or a real-looking API key.

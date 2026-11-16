# Token tips for new Claude Code users

Every message you send makes Claude re-read the whole conversation so far. Long
sessions get expensive, so the cheapest token is the one never added.

## Habits that help most
- **One task per session.** Start a new chat with `/clear` when you switch to unrelated work.
- **`/compact` when a long task is half done.** It replaces the history with a summary.
- **Be specific.** "Fix the date bug in `app/util.js` `parseDate()`" costs far less than
  "something is wrong with dates". Name files, functions and the exact error.
- **Paste the shortest useful error**, not the full log.
- **Ask for a plan first on big changes.** Fixing a wrong plan is cheaper than fixing wrong code.

## Choose the right model
- **Haiku:** searching, renaming, tagging, simple lookups.
- **Sonnet:** most coding, debugging, research.
- **Opus:** planning, hard judgement, reviewing tricky changes.
- **Fable:** only the biggest, hard-to-undo decisions (if you have access).

## Keep fixed costs small
- `CLAUDE.md` is read on every turn. Keep it under about 80 lines; point to other files
  instead of copying them in.
- Keep `CODEMAP.md` fresh (`/map`) so Claude finds code without opening files.
- Deny rules in `.claude/settings.json` stop Claude reading `node_modules`, build output
  and lock files. They are a helper, not a security wall: keep secrets out of the project.

## When subagents cost more, not less
Each subagent starts with its own fresh context. They save tokens only when they read
a lot and return a little. Do it yourself when:
- you already know the exact file and line;
- the job is a single quick command;
- you would need to paste most of the conversation into the subagent's task.

## Measure, don't guess
`python scripts/measure_tokens.py` shows the real token counts of your last session,
including subagents. Compare the same task done two ways before believing any claim,
including ours.

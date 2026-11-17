---
name: learn-corrections
description: "Save a repeated correction or 'always/never' preference as a rule (/learn)."
---

# learn-corrections

Rules live in `.claude/LEARNED.md`. `CLAUDE.md` imports it with the line
`@.claude/LEARNED.md`, so every new session follows them without being told again.

## When to record
- The user corrects the same kind of thing for the second time.
- The user states a standing preference ("always use tabs", "never touch tests").
- The user types `/learn <rule>`.
Don't record one-off instructions for the current task.

## How to record
1. Write the rule as one short, direct line, plus the reason if the user gave one:
   `- Use pathlib, not os.path, for new code. (user: easier to read)`
2. Put it under the right heading in `.claude/LEARNED.md`
   (`Code style`, `Fixing bugs`, `Testing`, `Workflow`, `Don't`).
   Create the file from the template in the kit if it is missing, and add
   `@.claude/LEARNED.md` to CLAUDE.md if that line is missing.
3. If a rule on the same topic exists, replace it; never keep two rules that conflict.
4. Keep the file under 40 rules. When it's full, merge similar rules.
5. Tell the user in one line: `learned: <rule>`. They can say "forget that" to remove it.

## Never record
Personal details, names, emails, passwords, keys, tokens, client data, or anything
the user calls private. `.claude/LEARNED.md` may be committed and made public.

## If the rule is unclear
Ask one question before recording: "Should I always <X>, or only for <case>?"

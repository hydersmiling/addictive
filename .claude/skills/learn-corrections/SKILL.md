---
name: learn-corrections
description: "Save a repeated correction as a rule, or a repeated workflow as a project skill (/learn)."
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

## Growing a skill
A rule is one line. When what the user teaches is a whole procedure, it becomes a skill.

When to offer one:
- The user walks you through the same multi-step job a second time
  ("run the linter, then the tests, then update the changelog").
- The user says "whenever I ask for X, do Y" and Y has three or more steps.
- The user types `/learn skill <what it should do>`.
Don't offer one for a single step (that is a rule) or for a job done only once.

How to create it:
1. Check that no existing skill already covers the job; if one does, offer to extend it.
2. Propose it in two lines and wait for a yes:
   `Save this as skill "release-notes": 1) ... 2) ... 3) ...?`
3. On yes, write `.claude/skills/<name>/SKILL.md`: a lowercase hyphenated name, a
   `description:` of one short line saying when to use it, then the numbered steps in
   the user's own words. Keep it under 30 lines.
4. Never overwrite a core Mainseat skill. Keep at most 5 learned skills, because every
   skill's description is loaded on every turn; past that, offer to merge or retire one.
5. Tell the user in one line: `learned skill: <name>`. They can say "forget that skill"
   to delete it. Refer to the user as "they" in any file you write.

## Never record
Personal details, names, emails, passwords, keys, tokens, client data, or anything
the user calls private. `.claude/LEARNED.md` may be committed and made public.

## If the rule is unclear
Ask one question before recording: "Should I always <X>, or only for <case>?"

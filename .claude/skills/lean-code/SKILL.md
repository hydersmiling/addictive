---
name: lean-code
description: >
  Write the smallest correct change that does exactly what the user asked,
  nothing more. Use for any code change: features, fixes, refactors. Covers
  planning reads cheaply, reusing code, and trimming the result before you finish.
---

# lean-code

Fewer lines are cheaper to write, read, review and fix. The goal is the same
behaviour in less code, never clever or cramped code.

## Before writing
1. Restate the request in one line. Anything not in that line is out of scope.
   Unsure whether something is wanted? Ask; don't build it "just in case".
2. Find before you read: `CODEMAP.md`, then the `explorer` agent, then a targeted
   search. Read only the line ranges you need, not whole files.
3. Run the `reuse-first` skill before creating any file, function or dependency.

## While writing
- Change the fewest files and lines that fully solve the request.
- Use what the language, standard library and existing project code already give you.
- No new options, settings, abstractions, layers, wrappers or "future-proofing"
  unless the request needs them.
- Don't reformat, rename or tidy code you weren't asked to touch. Keep existing comments.
- Readable beats short: no one-letter names, no packed one-liners, no removed error handling.

## Before you say done
1. Look at your diff. For each added block ask: does the request need it? Delete it if not.
2. Could an existing helper replace any new code? Use it.
3. Run the `self-check` skill.
4. Report in one line: files changed, lines added and removed.

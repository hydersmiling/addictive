---
name: self-check
description: "Prove a change works with the narrowest test; debug failures."
---

# self-check

## After every change
1. Run the narrowest proof first: the test for the code you touched, or the
   exact command that showed the bug. Then the project's full test command if it
   is quick (see `Run tests` in CLAUDE.md).
2. If the project has a linter or type checker, run it on the changed files only.
3. Re-read your diff once, looking for: typos, unhandled errors, leftover debug
   prints, files changed by accident, secrets.

## When something fails
1. Read the **first** error, not the last. Copy its shortest decisive line.
2. Cross-check: does the error point at code you changed? Check that line first.
   If not, it may be an existing problem: say so instead of "fixing" unrelated code.
3. Fix only what the error shows. Re-run the same proof.
4. **Two failed attempts → stop guessing.** Hand it to the `debugger` agent with the
   error line, the command, and what you tried.
5. Debugger can't find it either → ask the user, or for a design-level problem use
   `big-decision`. Never loop on the same fix.

## Report
`checked: <command> -> pass | fail (<error line>)`, one line per check.
Never say "done" or "fixed" without a passing check, or say clearly that it is unverified and why.

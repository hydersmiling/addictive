---
name: split-file
description: "Split a file or function that has grown too big, keeping every import working (/split-file)."
---

# split-file

Big files cost tokens every time they are read and are risky to change. Split them by
responsibility, so each future task opens only the part it needs.

## When
- `python scripts/find_large.py` lists the file (over ~400 lines) or function (over ~80), or
- you keep re-reading the same large file across tasks.
Skip data files, generated code and files that are long but simple (a list of constants).

## Steps
1. Run the tests and note the result. No tests cover the file? Write a quick one for its
   public behaviour first, or tell the user the split is unverified.
2. Group the contents by responsibility (parsing, storage, formatting...). Aim for files of
   100-300 lines with one clear job each. Name files after that job.
3. Move one group at a time. **Keep every public name importable from its old location**
   by re-exporting it there, so no caller has to change in the same step.
4. Run the tests after each move. Stop and undo the last move if anything fails.
5. When everything passes, update callers to the new locations only if the user wants
   that; otherwise the re-exports stay. Run `/map` so the code map shows the new files.

## Language details (read only the one you need)
- Python: `${CLAUDE_SKILL_DIR}/references/python.md`
- JavaScript and TypeScript: `${CLAUDE_SKILL_DIR}/references/javascript.md`

## Report
`split: <old file> -> <new files>; re-exports kept in <old file>; tests: pass`

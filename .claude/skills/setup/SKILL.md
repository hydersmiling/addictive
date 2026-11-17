---
name: setup
description: >
  One-time Mainseat setup for the current project after installing the plugin. Adds
  CLAUDE.md (the routing rules), .claude/settings.json, .claude/LEARNED.md and the code
  map and token scripts. Use when the user types /mainseat:setup or asks to set up Mainseat.
disable-model-invocation: true
---

# Mainseat setup

The plugin already provides the agents and skills. This step adds the per-project files
that make the routing work. It never overwrites a file that already exists.

1. Find the installer: it is `scripts/install.py` three folders above this skill's base
   directory (the plugin root), i.e. `<base directory>/../../../scripts/install.py`.
2. From the project root, preview: `python "<installer path>" . --rules-only --dry-run`
   and show the user the list of files it would add.
3. If the user agrees, run it without `--dry-run`.
4. Ask the user for one line describing the project and the command that runs its tests,
   and write them into the two placeholder lines at the top of `CLAUDE.md`.
5. Build the map: `python scripts/make_codemap.py`.
6. Finish with one line: setup is done, and the session is best run on Sonnet
   (`claude --model sonnet`).

If `CLAUDE.md` already exists, the installer skips it: offer to merge the "Who does what"
and "Every change" sections from the template by hand instead.

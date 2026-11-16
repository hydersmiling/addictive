# Addictive

A small "brain" kit for Claude Code that tries to spend fewer tokens without lowering quality:

- **Opus thinks, cheaper models fetch.** Haiku finds code, Sonnet makes small edits, Opus plans and decides.
- **A code tree.** `CODEMAP.md` lists files and what they do, so Claude can find things without opening them.
- **Check before you create.** Search for existing code before writing new code.

**Status:** design stage. Nothing is measured yet, so this README makes no savings claims.
See [docs/DESIGN.md](docs/DESIGN.md) and [docs/RESEARCH.md](docs/RESEARCH.md).

## What's inside today
- `.claude/skills/`: terse-output and working-style skills from [caveman](https://github.com/JuliusBrussee/caveman).
- `.claude/agents/`: read-only scout, small-edit builder and diff reviewer agents, also from caveman.

## Credits
Skills and agents in `.claude/` come from [caveman](https://github.com/JuliusBrussee/caveman) by
Julius Brussee, Apache License 2.0. See [third_party/caveman/SOURCE.md](third_party/caveman/SOURCE.md)
for what was copied and changed. Not affiliated with or endorsed by the caveman project.

## Licence
Our own code: MIT (to be added with v1). Third-party files keep their own licences.

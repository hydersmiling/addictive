# References

Mainseat follows Anthropic's published guidance for Claude Code. This page lists the sources
and what Mainseat does because of each one. The wording here is ours; read the originals for
the full picture.

## Sources
- **Claude Code in Action**, Anthropic Academy course:
  https://anthropic.skilljar.com/claude-code-in-action
- **Skills**, Claude Code documentation: https://code.claude.com/docs/en/skills
- **Best practices**, Claude Code documentation: https://code.claude.com/docs/en/best-practices
- **Subagents**, Claude Code documentation: https://code.claude.com/docs/en/sub-agents
- **Plugins reference**, Claude Code documentation: https://code.claude.com/docs/en/plugins-reference

## What Mainseat adopts
| Guidance | Where Mainseat applies it |
|---|---|
| Keep `CLAUDE.md` lean; it is read on every turn | The template is about 360 tokens; long procedures live in skills |
| Move repeated procedures into skills so they load only when used | Every workflow is a skill; descriptions are one line |
| Keep a `SKILL.md` under 500 lines; put depth in supporting files that load on demand | `split-file` keeps language detail in `references/`; `check_agents.py` fails a core skill over 500 lines |
| Keep a skill's name and description short (the listing is truncated) | `check_agents.py` fails a core skill whose name and description exceed 1,536 characters |
| Use subagents to keep heavy reading out of the main conversation; ask for short results | `explorer` returns `path:line` citations; helpers are used only for big jobs |
| Use cheaper models for simple subagent work | Haiku for searches, noisy commands and reviews; Sonnet as the main model |
| Steer long sessions: `/clear` between unrelated tasks, `/compact` with a focus | Token tips and the README's "keep sessions short" advice |
| Plan before large changes | `planner` writes the plan for multi-file work |
| Rules that must always hold belong in deny rules or hooks, not in prose | `.claude/settings.json` denies secret files; Mainseat ships no hooks by choice |
| Verify work instead of trusting it | `self-check` runs the narrowest test; benchmarks use hidden checks |

## Mainseat's own additions (not from the sources above)
- Splitting big files with re-exports so imports keep working (`split-file`, `scripts/find_large.py`).
- Measured routing: Sonnet in the main seat, Opus for planning and showcase pages, backed by
  the runs in `docs/BENCHMARK.md`.

The course's lesson pages require an account; only its public outline was consulted. If a
source changes, update this page and the matching rule.

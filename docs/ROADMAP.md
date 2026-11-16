# Roadmap

Goal: a new Claude Code user installs one kit and gets a well-set-up, token-aware
Claude that can plan, build, debug, review and research. Each step ships only
after it is tested.

## Done (v1)
- Code map script with secret filtering, `.gitignore` support and a stale check.
- Token counter that reads Claude Code's own logs, including subagents.
- Agents: scout (Haiku), builder (Sonnet), reviewer (Haiku), debugger (Sonnet),
  researcher (Sonnet), big-decision (Fable, rare).
- Third-party terse skills for short replies and working styles; `/map` skill.
- CLAUDE.md template, deny rules, installer that never overwrites, header checker, CI.
- Skills: `lean-code`, `reuse-first`, `self-check` (with escalation after two failed fixes),
  `learn-corrections` + `.claude/LEARNED.md`; optional `code-graph`; MCP guide.

## Next, in priority order
1. **Benchmark.** 3-5 fixed tasks on 2-3 small sample repos, run with and without the
   kit using `claude -p`. Record tokens *and* pass/fail. Publish the method and raw
   numbers, as ranges. No savings claim before this exists.
2. **Doctor script.** One command that checks CLAUDE.md length, map freshness, deny
   rules, agent headers and Fable access, and prints plain-English fixes.
3. **Symbol map for more languages.** Function and class names for JS/TS, Go, Java
   (start with simple regexes; tree-sitter only if needed).
4. **Hooks (opt-in).** Refresh the map at session start; warn when CLAUDE.md grows past
   80 lines. Off by default.
5. **More skills for new users:**
   - `tdd`: write a failing test, make it pass, stop.
   - `explain-code`: plain-English tour of a file or feature for beginners.
   - `commit`: small, well-described commits, no secrets.
   - `security-check`: quick scan for secrets and risky patterns before pushing.
   - `onboard`: first-run tour that builds the map and fills in CLAUDE.md.
6. **Measure the learning loop.** Count how often the same correction comes back after it
   was recorded in `.claude/LEARNED.md`.
7. **Plugin packaging.** One-command install through a Claude Code plugin marketplace.
8. **Prompt cookbook.** Vague vs. specific prompts with measured token counts.
9. **Before/after examples** in the README from the benchmark.

## Not planned
- A proxy or engine that rewrites API traffic (one of our sources has one; too big and risky here).
- Anything that sends project code to a third-party service.

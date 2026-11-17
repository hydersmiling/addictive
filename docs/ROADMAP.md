# Roadmap

## Next
1. **Cut lookup overhead.** Run 2 (64 files, Opus) showed equal quality, smaller diffs and
   +0-6% tokens, but +21% on lookups. Make map reading cheaper, then rerun with `--repeat 3`.
2. **Doctor command.** Check `CLAUDE.md` length, map freshness, deny rules, agent headers and
   Fable access; print fixes.
3. **Symbols for more languages.** JS/TS, Go, Java in the code map.
4. **Opt-in hooks.** Refresh the map at session start; warn on a long `CLAUDE.md`.
5. **Skills.** `tdd`, `explain-code`, `commit`, `security-check`, `onboard`.
6. **Measure the learning loop.** How often a recorded correction recurs.
7. **Plugin packaging.** One-command install from a plugin marketplace.

## Out of scope
- Proxies that intercept or rewrite API traffic.
- Anything that sends project code to a third-party service.

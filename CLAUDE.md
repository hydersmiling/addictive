# Mainseat: project rules

Token-efficient orchestration kit for Claude Code (public: github.com/musahyderr/mainseat).
Read this file; open other files only when the index below says so.

## IMPORTANT (read every time)
1. `git fetch` and compare with `origin/main` before starting: other sessions also release.
2. Every change reaches `main` through a pull request. Merge **locally** with the repo's noreply
   identity, never with GitHub's merge button (it stamps a personal email). CI must pass on
   Linux, Windows and macOS.
3. Never commit secrets, session logs, benchmark results or personal details
   (`tests/test_privacy_guard.py` enforces this). `benchmarks/results/` stays local.
4. No savings or quality claim without a measured run recorded in `docs/BENCHMARK.md`.
   Show new results to the user privately before publishing them.
5. Every agent states `model:` and `tools:`; descriptions are one line. Run
   `python scripts/check_agents.py` after touching `agents/` or `.claude/skills/`.
6. Third-party files: log every change in `third_party/skills/SOURCE.md`.
7. On this Windows machine: edit text with Python or the editor (never PowerShell
   `Get-Content`/`Set-Content`); no backslash escapes inside heredocs; screenshots run
   from PowerShell (the Bash sandbox blocks the browser).
8. Verify a release by installing it the way a user would, not only by validating it.
9. Code: plain, commented Python, standard library only. Do small jobs yourself; use helpers
   only for big searches (`explorer`), noisy commands (`runner`) and large diffs (`reviewer`).

## Where things are (open only when needed)
| Open | When |
|---|---|
| `README.md` | Changing what users see first (install, results, options) |
| `INSTALL.md` | Changing install steps (also read by other Claudes given the repo link) |
| `CLAUDE.md.template` | Changing the rules Mainseat installs in users' projects |
| `agents/`, `.claude/skills/`, `.claude/README.md` | Changing an agent or skill |
| `scripts/` | Changing a tool (installer, map, token counter, find_unused, find_large, screenshot) |
| `benchmarks/` + `docs/BENCHMARK.md` | Running or reporting a benchmark |
| `docs/LESSONS.md` | Only when a problem resembles one listed there; add an entry when something breaks |
| `docs/GUIDE.md` | Long-form user guide (walkthroughs, FAQ, troubleshooting) |
| `docs/DESIGN.md`, `docs/REFERENCES.md` | Design decisions and the Anthropic guidance they follow |
| `docs/PRIVACY.md`, `docs/MCP.md`, `docs/token-tips.md`, `docs/ROADMAP.md` | Their topic only |
| `CHANGELOG.md`, `.claude-plugin/plugin.json` | Releasing: bump both versions together (a test checks) |

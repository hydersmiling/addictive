# Research notes: Claude Starter Kit ("addictive")
Date: 2026-11-17. Input: "Claude Starter Kit: Handoff Brief for Opus" (Nov 16, 2026).

## 1. Open-source projects worth borrowing from

| Project | What it does | Use in our kit | Caveat |
|---|---|---|---|
| **Terse-output skill pack** (Apache-2.0, now in `third_party/skills`) | Short-reply mode, notes compressor, session stats from the JSONL logs | We copied its skills and agents (renamed). Its stats approach (read the JSONL logs) is how our token counter works | Headline 65-75% is output tokens only; independent testers find ~1-4% of a whole session bill |
| **ccusage** (ryoppippi/ccusage, MIT) | Reads local `~/.claude/projects/**/*.jsonl` and reports tokens/cost per session | Benchmark harness: run task with/without kit, compare with ccusage or our own small JSONL reader | One source says it may skip subagent JSONL files (`<session>/subagents/*.jsonl`); we must count those, or subagent cost is hidden |
| **Aider repo map / RepoMapper** | Tree-sitter symbols ranked by PageRank | Model for the v2 "symbol-aware map" | Heavier dependency; keep v1 stdlib-only |
| **tokenmiser** (phlx0/tokenmiser) | Writes CODEBASE_INDEX.md + pointer in CLAUDE.md | Nearly identical to our make_codemap idea, so it's direct competition; read it before writing ours and say how we differ in the README | Author-claimed 50-80% |
| **Stacklit** | Committed JSON module map via tree-sitter | Its comparison of Repomix / code2prompt / Aider is a useful README reference | Written by its own author |
| **Code knowledge-graph tool** (Apache-2.0, optional `optional/code-graph`), codebase-memory-mcp, code-review-graph | Graphs Claude queries instead of grepping | Included as an optional skill for large repos | Large setup; claims are vendor benchmarks |
| **rtk** | CLI proxy compressing command output (test logs, git) | Optional tip in token-tips.md | Vendor 60-90% claim |
| **Repomix** | Packs whole repo into one prompt | Use as the counter-example: ~800k tokens on FastAPI vs ~10k for a map | One author's test |

## 2. Corrections to the brief (from current official docs)

- **Built-in Explore subagent already exists** (read-only, skips CLAUDE.md). Our `explorer` overlaps it. Option: name ours `Explore` with `model: haiku` to override the built-in. That's one line and it's a real, measurable change; good beginner-friendly selling point.
- **Agent frontmatter**: only `name` and `description` are required. Useful extras: `tools`, `disallowedTools`, `model` (haiku/sonnet/opus/fable/inherit/full ID), `effort`, `maxTurns`, `omitClaudeMd`, `color`. Unknown fields are silently ignored, so the planned CI frontmatter validator is worth building.
- **Deny rules** use gitignore syntax: `Read(.env)` matches at any depth; `./` = relative to cwd, `/` = relative to the settings file's project, `//` = absolute. A Read deny also blocks Edit/Write.
- **Deny rules and subagents**: docs say custom subagents have "independent permissions"; several open bug reports say project deny rules weren't enforced in subagents or when launched from a subdirectory. **So the kit must not promise deny rules = secrets safe.** Also give `explorer` `disallowedTools` and keep secrets out of CODEMAP.md (already in brief).
- **Measurement must include subagent JSONL files**, otherwise "explorer saved tokens" is a false claim (brief's own risk #2).

## 3. Suggested v1 changes
1. Read tokenmiser first; differentiate on *measured* results + beginner docs + staleness check.
2. Ship `explorer` as an override of built-in `Explore` with `model: haiku`, `maxTurns` cap, 200-word summary rule.
3. Add a tiny `scripts/measure_tokens.py` (stdlib, reads JSONL incl. subagents) to v1, because the success metric needs it anyway; ccusage as the cross-check.
4. Keep the third-party skills as plain files we can read and edit, not a plugin dependency.

## Sources
- Third-party skill sources: see `third_party/skills/NOTICE`
- https://www.mintlify.com/ryoppippi/ccusage , https://www.faros.ai/blog/claude-code-token-usage
- https://github.com/phlx0/tokenmiser , https://github.com/glincker/stacklit/discussions/13
- https://dev.to/thegdsks/i-tested-4-codebase-to-ai-tools-on-fastapi-108k-lines-here-are-the-token-costs-4bmc
- https://www.deployhq.com/blog/free-github-repos-for-claude-code
- https://code.claude.com/docs/en/sub-agents , https://code.claude.com/docs/en/settings , https://code.claude.com/docs/en/permissions
- https://claudeissues.com/issue/27000-bug-project-settings-json-deny-rules-not-enforced-in-task-subagents

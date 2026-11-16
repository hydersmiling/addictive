# Recommended MCP servers

An MCP server gives Claude extra tools (a browser, docs search, and so on).
**Every server you add has a token cost:** its tool descriptions are loaded into
the session. So add only what you will really use, and remove what you don't.

Add a server for one project (stored in `.mcp.json`, shareable with your team):
```bash
claude mcp add --scope project <name> -- <command>
```
List or remove: `claude mcp list`, `claude mcp remove <name>`.

## Start with these
| Server | Why it saves tokens or time | Add it |
|---|---|---|
| **Context7** | Fetches current docs for a library version instead of Claude guessing or loading whole web pages. Pairs with the `researcher` agent. | `claude mcp add context7 -- npx -y @upstash/context7-mcp` |
| **Playwright** | Lets Claude open your web app, click through it and read errors: real debugging of front-end bugs. | `claude mcp add playwright -- npx -y @playwright/mcp@latest` |

## Add when you need them
| Server | When |
|---|---|
| **Chrome DevTools MCP** (`npx -y chrome-devtools-mcp@latest`) | Deeper web debugging: console, network requests, performance traces. Pick this *or* Playwright, rarely both. |
| **Code graph** (`/code-graph --mcp`, from the optional `code-graph` skill) | Large codebases where `CODEMAP.md` gets too long. Lets Claude query the graph instead of grepping. |
| **Sentry**, **Linear/Jira** | Only if your team already uses them; Claude can read the real error or ticket. |

## Usually skip
- **GitHub MCP:** the `gh` command-line tool does the same with no tool descriptions loaded. Install `gh` instead.
- **Filesystem / git / fetch MCPs:** Claude Code already has these built in.
- **"Memory" MCPs:** this kit uses plain files (`CODEMAP.md`, `.claude/LEARNED.md`) that you can read and edit.

## Safety
- Only add servers from sources you trust; a server can read what you give it.
- Never paste API keys into `.mcp.json` if you commit it. Use environment variables.
- Check package names carefully before running `npx`: look-alike names exist.

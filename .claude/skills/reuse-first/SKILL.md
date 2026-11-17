---
name: reuse-first
description: "Check for existing code or a library before creating anything new."
---

# reuse-first

Duplicate code costs tokens twice: once to write it, again every time someone
has to read both copies. Search first; it is far cheaper than building.

## Steps (stop at the first step that finds a fit)
1. **Map.** Search `CODEMAP.md` for the name and 2-3 synonyms
   (e.g. "parse date" → `parse`, `date`, `time`, `format`). Match whole words.
2. **Scout.** Ask the `explorer` agent one precise question:
   "Is there existing code that <does X>? Return path:line or no match."
   For a wide search, run 2 `explorer` calls at once with different angles (definitions vs. callers).
3. **Confirm a "no match".** Do one direct search yourself (Grep for the key word)
   before believing it. Scouts can miss.
4. **Dependencies.** Check the project's dependency file (`requirements.txt`,
   `pyproject.toml`, `package.json`, `go.mod`, ...) for a library already installed
   that does it.
5. **Standard solution.** Still nothing and the task is common (dates, CSV, retries,
   validation)? Ask the `researcher` agent for the standard-library or well-known way.
   Never send project code or private details in a web search.

## Then decide, in one line
- `reuse: <path:line>`: call it as is.
- `extend: <path:line>`: small change to existing code (keep its callers working).
- `new: <path>`: nothing fits; say why in a few words. After creating it, refresh the map (`/map`).

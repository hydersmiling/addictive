---
name: map
description: >
  Refresh CODEMAP.md, the project's file map. Use when the user types /map,
  after creating, moving or deleting files, or when the map check reports STALE.
---

# map

1. Run `python scripts/make_codemap.py` from the project root.
   If the script is missing, tell the user to copy it from the Mainseat kit.
2. Report its one-line result. Do not print the map.
3. If a file you expected is missing from the map, it is either gitignored or
   looks like a secret. That is on purpose; do not work around it.

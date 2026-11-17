---
name: map
description: "Refresh CODEMAP.md (/map) after adding, moving or deleting files."
---

# map

1. Run `python scripts/make_codemap.py` from the project root.
   If the script is missing, tell the user to copy it from the Mainseat kit.
2. Report its one-line result. Do not print the map.
3. If a file you expected is missing from the map, it is either gitignored or
   looks like a secret. That is on purpose; do not work around it.

"""A stand-in reviewer for tests: always prefers solution A. Never calls any service."""

import json

verdict = {"A": {"correctness": 9, "readability": 8, "minimal_scope": 9, "fits_codebase": 8},
           "B": {"correctness": 7, "readability": 6, "minimal_scope": 5, "fits_codebase": 6},
           "better": "A", "reason": "A is smaller and reuses helpers."}
print(json.dumps({"type": "result", "result": json.dumps(verdict)}))

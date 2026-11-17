"""A stand-in visual judge for tests: always ranks A first. Never calls any service."""

import json

verdict = {"scores": {"A": {"visual_quality": 9, "polish": 9, "brand_fit": 9, "completeness": 9},
                      "B": {"visual_quality": 6, "polish": 6, "brand_fit": 6, "completeness": 6},
                      "C": {"visual_quality": 3, "polish": 3, "brand_fit": 3, "completeness": 3}},
           "ranking": ["A", "B", "C"], "reason": "A looks most finished."}
print(json.dumps({"type": "result", "result": json.dumps(verdict), "total_cost_usd": 0.0}))

"""A stand-in for `claude -p` used only by tests. It never calls any service.

It fixes the sample repo's bug when asked about failing tests, answers the
"locate" question, and prints JSON shaped like Claude Code's --output-format json.
"""

import json
import sys

prompt = sys.argv[sys.argv.index("-p") + 1] if "-p" in sys.argv else ""
answer = "done"
if "tests fail" in prompt:
    path = "shop/cart.py"
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    text = text.replace("sum(cents for _name, cents, _q in cart.items)",
                        "sum(cents * q for _name, cents, q in cart.items)")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
elif "Which file" in prompt:
    answer = "shop/cart.py calc_total"

print(json.dumps({"type": "result", "result": answer, "total_cost_usd": 0.0,
                  "num_turns": 1, "session_id": None, "is_error": False}))

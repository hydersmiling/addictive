"""Hidden check: calc_line_total must be gone everywhere; line_total must work."""

import pathlib
import sys

sys.path.insert(0, ".")
left = [str(p) for p in pathlib.Path(".").rglob("*.py")
        if p.name != "check_rename_large.py" and "calc_line_total" in p.read_text(encoding="utf-8")]
if left:
    sys.exit(f"calc_line_total still in: {left}")
from depot.orders.lines import line_total  # noqa: E402
from depot.orders.pricing import subtotal  # noqa: E402
from tests.helpers import make_order  # noqa: E402

order = make_order(quantity=2)
sys.exit(0 if line_total(order.lines[0]) == 2000 and subtotal(order) == 2000 else "wrong totals")

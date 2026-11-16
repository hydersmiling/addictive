"""Hidden check for the rename task: calc_total must be gone, cart_total must work."""

import pathlib
import sys

sys.path.insert(0, ".")
leftovers = [str(p) for p in pathlib.Path(".").rglob("*.py")
             if "hidden_" not in p.name and "calc_total" in p.read_text(encoding="utf-8")]
if leftovers:
    sys.exit(f"calc_total still in: {leftovers}")
from shop.cart import Cart, cart_total  # noqa: E402

c = Cart()
c.add("apple", 150)
sys.exit(0 if cart_total(c) == 150 else "cart_total gave the wrong answer")

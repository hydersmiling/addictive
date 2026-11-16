"""Hidden check: order_summary output (copied in only after Claude finishes)."""

import unittest

from depot.reports.sales_report import order_summary
from tests.helpers import make_order


class OrderSummaryTests(unittest.TestCase):
    def test_summary(self):
        order = make_order(quantity=3)  # 3 x $10.00, standard tier, 8% tax -> $32.40
        self.assertEqual(order_summary(order), f"Order {order.order_id}: 3 items, total $32.40")


if __name__ == "__main__":
    unittest.main()

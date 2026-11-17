import unittest
from datetime import date

from depot.api.auth import is_authorised
from depot.core.dates import month_bounds
from depot.inventory.batches import expiring_before
from depot.inventory.reorder import needs_reorder
from depot.inventory.stock import Stock
from depot.notifications.templates import render


class MiscTests(unittest.TestCase):
    def test_auth(self):
        self.assertTrue(is_authorised("abc", "abc"))

    def test_month_bounds(self):
        self.assertEqual(month_bounds(date(2026, 2, 10))[1], date(2026, 2, 28))

    def test_expiring(self):
        self.assertEqual(len(expiring_before([{"expires": date(2026, 1, 1)}], date(2026, 6, 1))), 1)

    def test_reorder(self):
        self.assertTrue(needs_reorder(Stock(), "ABC-0001", daily_sales=2, lead_time_days=5))

    def test_template(self):
        self.assertIn("ORD-1", render("shipped", name="Ada", order_id="ORD-1"))

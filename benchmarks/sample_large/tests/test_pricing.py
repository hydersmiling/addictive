import unittest

from tests.helpers import make_order
from depot.orders.pricing import subtotal, total


class PricingTests(unittest.TestCase):
    def test_subtotal(self):
        self.assertEqual(subtotal(make_order(quantity=3)), 3000)

    def test_standard_total_includes_tax(self):
        self.assertEqual(total(make_order()), 1080)

    def test_gold_at_threshold_gets_ten_percent(self):
        self.assertEqual(total(make_order(points=1000)), 972)

    def test_silver_discount(self):
        self.assertEqual(total(make_order(points=700)), 1026)

    def test_bulk_discount(self):
        self.assertEqual(total(make_order(quantity=20, cents=100)), 2095)

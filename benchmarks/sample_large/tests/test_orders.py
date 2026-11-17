import unittest
from datetime import date

from tests.helpers import make_order
from depot.inventory.stock import Stock
from depot.orders.fulfillment import pick, ship_date
from depot.orders.invoices import invoice_text
from depot.orders.returns import refund_for


class OrderTests(unittest.TestCase):
    def test_pick(self):
        order = make_order(quantity=2)
        stock = Stock()
        stock.receive("ABC-0001", 5)
        pick(order, stock)
        self.assertEqual((order.status, stock.on_hand("ABC-0001")), ("picked", 3))

    def test_ship_date_skips_weekend(self):
        self.assertEqual(ship_date(date(2026, 1, 2)), date(2026, 1, 7))

    def test_refund(self):
        self.assertEqual(refund_for(make_order(quantity=2).lines[0]), 1800)

    def test_invoice(self):
        self.assertIn("Total: $10.80", invoice_text(make_order()))

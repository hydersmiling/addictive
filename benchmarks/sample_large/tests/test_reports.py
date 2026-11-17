import unittest

from tests.helpers import make_order
from depot.inventory.stock import Stock
from depot.reports.daily import daily_summary
from depot.reports.export_csv import to_csv
from depot.reports.stock_report import stock_report


class ReportTests(unittest.TestCase):
    def test_daily(self):
        self.assertEqual(daily_summary([make_order(), make_order()]), "2 orders, revenue $21.60")

    def test_stock_report(self):
        s = Stock()
        s.receive("ABC-0001", 7)
        self.assertIn("ABC-0001", stock_report(s))

    def test_csv(self):
        self.assertEqual(to_csv([[1, 2]], ["a", "b"]).splitlines(), ["a,b", "1,2"])
